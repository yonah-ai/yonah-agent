#!/usr/bin/env bash
# One-command deploy for yonah-agent.
# Deploys the Chalice REST + WebSocket API; the worker is built by AWS
# CodeBuild and updated separately when the buildspec.yml finishes.
#
# Prereqs: see DEPLOY.md (AWS CLI configured, DynamoDB tables created,
# SQS queues created, KMS CMK provisioned, Chalice installed).

set -euo pipefail

STAGE="${1:-prod}"
AWS_REGION="${AWS_REGION:-us-east-1}"
NAME_PREFIX="${NAME_PREFIX:-yonah}"

echo "Deploying Chalice app to stage=$STAGE region=$AWS_REGION prefix=$NAME_PREFIX..."

# Sanity-check the stage config exists
if [ ! -f ".chalice/config.json" ]; then
    echo "ERROR: .chalice/config.json missing. Run 'chalice new-project .' first," >&2
    echo "       or copy from .chalice/config.example.json (see DEPLOY.md §6)." >&2
    exit 1
fi

chalice deploy --stage "$STAGE" --no-autogen-policy

echo "Chalice deploy complete."
echo "Worker image is built+pushed by AWS CodeBuild on git push to main."
echo "To update the worker Lambda to the latest ECR image, run:"
echo "  aws lambda update-function-code \\"
echo "    --function-name ${NAME_PREFIX}-worker \\"
echo "    --image-uri \$ACCOUNT_ID.dkr.ecr.\$AWS_REGION.amazonaws.com/${NAME_PREFIX}-worker:latest"
