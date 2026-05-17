# DEPLOY.md — AWS install guide for `yonah-agent`

This guide assumes a single-region deployment of the Yonah framework
upstream into an existing AWS account. The framework default
resource-name prefix is `yonah`; vertical forks override this via the
`NAME_PREFIX` environment variable to `{vertical}-yonah` (e.g.
`edu-yonah`, `health-yonah`, `hire-yonah`) so multiple verticals can
coexist in the same account without collision.

## 1. Prerequisites

- AWS account with permission to create IAM, DynamoDB, Simple Queue
  Service (SQS), Key Management Service (KMS), Lambda, API Gateway, and
  CodeBuild resources
- AWS CLI v2 configured (`aws configure`) with a profile that has the
  above permissions
- Docker (for the worker container image)
- Python 3.12 + a virtual environment
- `chalice` (`pip install chalice>=1.31`)
- `jq` (for inline JSON munging in the snippets below)

```bash
aws --version              # >= 2.x
docker --version           # >= 24.x
python3 --version          # >= 3.12
chalice --version          # >= 1.31
jq --version               # >= 1.6
```

## 2. Variables you will reuse

Set these once per deploy. Vertical forks override `NAME_PREFIX` to
their `{vertical}-yonah` value.

```bash
export AWS_REGION=us-east-1
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export STAGE=prod
export NAME_PREFIX=yonah   # vertical fork sets this to e.g. edu-yonah
```

## 3. IAM bootstrap

Apply the IAM role used by the Chalice Lambda(s) and the worker Lambda.
The repo ships `iam-policy.json` (TODO: pin to your account); update
the Amazon Resource Names (ARNs) to your resources before applying.

```bash
cat > /tmp/trust-policy.json <<'JSON'
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": { "Service": "lambda.amazonaws.com" },
    "Action": "sts:AssumeRole"
  }]
}
JSON

aws iam create-role \
  --role-name ${NAME_PREFIX}-lambda-role \
  --assume-role-policy-document file:///tmp/trust-policy.json

aws iam put-role-policy \
  --role-name ${NAME_PREFIX}-lambda-role \
  --policy-name ${NAME_PREFIX}-inline \
  --policy-document file://iam-policy.json
```

## 4. DynamoDB tables (seven DAOs)

```bash
aws cloudformation deploy \
  --stack-name ${NAME_PREFIX}-tables \
  --template-file cloudformation/dynamodb-tables.yml \
  --parameter-overrides NamePrefix=${NAME_PREFIX} \
  --region ${AWS_REGION}
```

The `cloudformation/dynamodb-tables.yml` file (TODO: ship in this repo)
provisions:

| DAO | Table name | PK | SK | GSIs |
|---|---|---|---|---|
| UserDao | `${NAME_PREFIX}-users` | `user_id` | — | — |
| ApiKeyDao | `${NAME_PREFIX}-api-keys` | `key_hash` | — | `user_id-index` |
| CohortDao | `${NAME_PREFIX}-cohorts` | `cohort_id` | `user_id` | `user_id-index` |
| ArtefactDao | `${NAME_PREFIX}-artefacts` | `user_id` | `artefact_id` | `cohort_id-index` |
| DecisionDao | `${NAME_PREFIX}-decisions` | `user_id` | `decision_id` | `cohort_id-index` |
| EnvelopeDao | `${NAME_PREFIX}-envelopes` | `decision_id` | `seq#step_id` | — |
| PiiTokenDao | `${NAME_PREFIX}-pii-tokens` | `decision_id` | `code` | TTL on `expires_at` |

The `EnvelopeDao` table is append-only by application contract; there
is no DynamoDB-level enforcement of that, so do not grant `DeleteItem`
to the worker role.

## 5. SQS queue + DLQ

```bash
aws sqs create-queue \
  --queue-name ${NAME_PREFIX}-evaluator-dlq \
  --attributes MessageRetentionPeriod=1209600

DLQ_ARN=$(aws sqs get-queue-attributes \
  --queue-url $(aws sqs get-queue-url --queue-name ${NAME_PREFIX}-evaluator-dlq --query QueueUrl --output text) \
  --attribute-names QueueArn --query 'Attributes.QueueArn' --output text)

aws sqs create-queue \
  --queue-name ${NAME_PREFIX}-evaluator-queue \
  --attributes "{
    \"VisibilityTimeout\": \"900\",
    \"MessageRetentionPeriod\": \"345600\",
    \"RedrivePolicy\": \"{\\\"deadLetterTargetArn\\\":\\\"${DLQ_ARN}\\\",\\\"maxReceiveCount\\\":3}\"
  }"
```

## 6. KMS CMK for PII tokens

```bash
aws kms create-key \
  --description "${NAME_PREFIX} PII-token encryption (per-tenant DEK wrapped by this CMK)" \
  --key-usage ENCRYPT_DECRYPT \
  --key-spec SYMMETRIC_DEFAULT \
  --tags TagKey=Project,TagValue=${NAME_PREFIX}

aws kms create-alias \
  --alias-name alias/${NAME_PREFIX}-pii-cmk \
  --target-key-id $(aws kms list-keys --query 'Keys[-1].KeyId' --output text)
```

## 7. Chalice config

```bash
cp .chalice/config.example.json .chalice/config.json
# Edit .chalice/config.json and replace TODO_* with the values from §2-§6:
#   - api_gateway_stage
#   - manage_iam_role: false
#   - iam_role_arn: arn:aws:iam::${AWS_ACCOUNT_ID}:role/${NAME_PREFIX}-lambda-role
#   - environment_variables:
#       NAME_PREFIX, AWS_REGION, EVALUATOR_QUEUE_URL, PII_KMS_KEY_ID
#   - automatic_layer: true (CrewAI is heavy)
```

## 8. Deploy the Chalice app

```bash
./deploy.sh ${STAGE}
```

This deploys the REST API + WebSocket API to API Gateway and creates
the Chalice Lambda functions.

## 9. Provision CodeBuild for the worker

The worker is a Docker image — too big for Chalice's standard Lambda
deploy. AWS CodeBuild builds and pushes the image to ECR; Lambda is
updated to point at the new tag.

```bash
./codebuild-setup.sh  # TODO: ship this script — creates the CodeBuild project,
                       # the ECR repo, and the source-build webhook
```

After the first build finishes:

```bash
aws lambda update-function-code \
  --function-name ${NAME_PREFIX}-worker \
  --image-uri ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${NAME_PREFIX}-worker:latest
```

## 10. Smoke test

Once everything is up, run the end-to-end smoke test:

```bash
./tests/smoke_test.sh https://YOUR_API_GATEWAY_URL/${STAGE}
```

The smoke test exercises the framework's seven-tool lifecycle:
`build_artefact` -> `publish_artefact` -> `tutor_me` (3 turns) ->
`submit_draft` -> `commit_decision` -> `query_my_provenance` ->
`delete_my_data`. It uses test API keys for one authority-audience
party and one second-audience party against a freshly-created cohort.
On success: every envelope hash chains, every structural verifier
passes, every tool invocation is logged in the PROV graph.

## 11. Local-only mode (no AWS)

For development without an AWS account, run against LocalStack:

```bash
docker run --rm -d -p 4566:4566 --name localstack localstack/localstack:latest
LOCALSTACK_ENDPOINT=http://localhost:4566 bash scripts/bootstrap_localstack.sh
LOCALSTACK_ENDPOINT=http://localhost:4566 chalice local
```

The `scripts/bootstrap_localstack.sh` script (TODO: ship) creates the
seven DynamoDB tables and the SQS queue inside LocalStack so the
application looks the same.

## 12. Tear-down

```bash
chalice delete --stage ${STAGE}
aws cloudformation delete-stack --stack-name ${NAME_PREFIX}-tables
aws sqs delete-queue --queue-url $(aws sqs get-queue-url --queue-name ${NAME_PREFIX}-evaluator-queue --query QueueUrl --output text)
aws sqs delete-queue --queue-url $(aws sqs get-queue-url --queue-name ${NAME_PREFIX}-evaluator-dlq --query QueueUrl --output text)
aws kms disable-key --key-id alias/${NAME_PREFIX}-pii-cmk
aws kms schedule-key-deletion --key-id alias/${NAME_PREFIX}-pii-cmk --pending-window-in-days 30
aws iam delete-role-policy --role-name ${NAME_PREFIX}-lambda-role --policy-name ${NAME_PREFIX}-inline
aws iam delete-role --role-name ${NAME_PREFIX}-lambda-role
```

## TODO before first deploy

- [ ] Ship `iam-policy.json` (least-privilege; reference the table/queue/key ARNs above)
- [ ] Ship `cloudformation/dynamodb-tables.yml`
- [ ] Ship `codebuild-setup.sh`
- [ ] Ship `scripts/bootstrap_localstack.sh`
- [ ] Ship `.chalice/config.example.json`
- [ ] Ship `tests/smoke_test.sh`
- [ ] Verify `jhcontext-sdk` and `jhcontext-protocol` versions on PyPI (pin in `pyproject.toml` once stable)
