# Lambda container image for the CrewAI worker.
# Built by AWS CodeBuild → pushed to ECR → consumed by Lambda.
FROM public.ecr.aws/lambda/python:3.12

# OS deps (kept minimal — no compiler unless a dep requires it)
RUN dnf -y install gcc && dnf clean all

WORKDIR ${LAMBDA_TASK_ROOT}

# Install Python deps first for layer caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Application code
COPY agent/    ./agent/
COPY chalicelib/ ./chalicelib/
COPY models/   ./models/
COPY worker/   ./worker/

# Entry point — SQS-triggered Lambda
CMD ["worker.worker_main.lambda_handler"]
