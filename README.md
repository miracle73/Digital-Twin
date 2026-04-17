# Digital Twin

An AI-powered digital twin chatbot that represents Miracle Nwadiaro professionally. Built with Gradio and the OpenAI SDK pointed at OpenRouter, with five callable tools (skills, experience, projects, contact, education) so the model answers career questions in first person from structured CV data.

Containerized with Docker, deployed to **AWS App Runner** via **Terraform** (IaC), shipped continuously with **GitHub Actions**.

---

## Architecture

```
                    ┌────────────────────────┐
                    │   GitHub (main push)   │
                    └───────────┬────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │    GitHub Actions      │
                    │  .github/workflows/    │
                    │      deploy.yml        │
                    └───────────┬────────────┘
                                │
            docker build + push │ aws apprunner start-deployment
                                ▼
┌──────────────┐      ┌────────────────────┐      ┌─────────────────────┐
│    ECR       │◄─────│   App Runner       │─────►│  Secrets Manager    │
│  digital-    │ pull │   1 vCPU / 2 GB    │ read │ openrouter-api-key  │
│  twin:<sha>  │      │   autoscale 1-3    │      └─────────────────────┘
└──────────────┘      │   port 7860        │
                      └──────────┬─────────┘
                                 │ logs
                                 ▼
                      ┌────────────────────┐
                      │   CloudWatch       │
                      │   Logs             │
                      └────────────────────┘
                                 │
                                 ▼
                      ┌────────────────────┐
                      │  Public HTTPS URL  │
                      │  (Gradio chat UI)  │
                      └────────────────────┘
```

**Request flow:** User → App Runner public HTTPS URL → Gradio (port 7860) → OpenAI SDK → OpenRouter (`openai/gpt-4o-mini`) → tool calls against local Python functions → reply.

---

## AWS Resources Provisioned

| Resource | Purpose |
|---|---|
| `aws_ecr_repository.app` | Private Docker registry for the image. Scan-on-push enabled, lifecycle rule keeps last 10 images. |
| `aws_secretsmanager_secret.openrouter_api_key` | Encrypted storage for `OPENROUTER_API_KEY`. Injected into the container as an env var. |
| `aws_iam_role.apprunner_ecr_access` | Access role. Lets App Runner pull from ECR (trust: `build.apprunner.amazonaws.com`). |
| `aws_iam_role.apprunner_instance` | Instance role. Attached to the running container so it can read the secret (trust: `tasks.apprunner.amazonaws.com`). |
| `aws_iam_policy.apprunner_instance_secrets` | Grants `secretsmanager:GetSecretValue` scoped to the single secret. |
| `aws_apprunner_auto_scaling_configuration_version.app` | Autoscaling: 1–3 instances, 100 concurrent requests per instance. |
| `aws_apprunner_service.app` | The service itself. 1 vCPU, 2 GB RAM, port 7860, wired to the secret and log group. |
| `aws_cloudwatch_log_group.app` | Retained application log group (`/aws/apprunner/digital-twin/application`, 14-day retention). App Runner additionally auto-creates its own service/application log groups under `/aws/apprunner/<service>/<id>`. |

---

## Run locally

Prerequisites: [uv](https://docs.astral.sh/uv/) and Python 3.11+.

```bash
# 1. Copy env template and fill in your OpenRouter key
cp .env.example .env
# edit .env and set OPENROUTER_API_KEY=sk-or-v1-...

# 2. Install deps and run
uv sync
uv run main.py
```

The Gradio UI starts on http://localhost:7860.

### Run in Docker locally

```bash
docker build -t digital-twin .
docker run --rm -p 7860:7860 -e OPENROUTER_API_KEY=sk-or-v1-... digital-twin
```

---

## Deploy to AWS

### One-time: Terraform bootstrap

Prerequisites:
- Terraform ≥ 1.5
- AWS CLI configured with an IAM user/role that can create ECR, IAM, Secrets Manager, CloudWatch, and App Runner resources
- An OpenRouter API key

```bash
cd terraform

# Fill in your real key
cp terraform.tfvars.example terraform.tfvars
# edit terraform.tfvars and set openrouter_api_key

terraform init
terraform fmt -check
terraform validate
terraform plan
terraform apply
```

The first `apply` will create the ECR repo but the App Runner service creation will fail/wait because there's no image in ECR yet. Two options:

**Option A — push an initial image manually, then apply:**
```bash
# Get ECR login
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin \
  $(aws sts get-caller-identity --query Account --output text).dkr.ecr.us-east-1.amazonaws.com

# Build & push
docker build -t digital-twin .
ECR_URL=$(cd terraform && terraform output -raw ecr_repository_url)
docker tag digital-twin:latest $ECR_URL:latest
docker push $ECR_URL:latest

# Now apply
cd terraform && terraform apply
```

**Option B — targeted apply:**
```bash
terraform apply -target=aws_ecr_repository.app
# Push an image as above, then:
terraform apply
```

### Configure GitHub Secrets for CI/CD

After `terraform apply` succeeds, capture outputs:

```bash
cd terraform
terraform output apprunner_service_arn
terraform output apprunner_service_url
```

Then add these **GitHub Actions secrets** (Settings → Secrets and variables → Actions):

| Secret | Value |
|---|---|
| `AWS_ACCESS_KEY_ID` | IAM user access key with ECR push + App Runner deploy permissions |
| `AWS_SECRET_ACCESS_KEY` | Matching secret key |
| `AWS_REGION` | `us-east-1` |
| `APP_RUNNER_SERVICE_ARN` | Output of `terraform output apprunner_service_arn` |

The minimum IAM permissions the CI user needs:
- `ecr:GetAuthorizationToken`, `ecr:BatchCheckLayerAvailability`, `ecr:CompleteLayerUpload`, `ecr:InitiateLayerUpload`, `ecr:PutImage`, `ecr:UploadLayerPart`, `ecr:BatchGetImage`
- `apprunner:StartDeployment`, `apprunner:DescribeService`

### Subsequent deploys

Every push to `main` triggers `.github/workflows/deploy.yml`, which:
1. Logs in to ECR
2. Builds the image for `linux/amd64`
3. Tags with both `:<commit-sha>` and `:latest` and pushes
4. Calls `aws apprunner start-deployment`
5. Polls `describe-service` until status is `RUNNING`

### Tear down

```bash
cd terraform && terraform destroy
```

---

## Project structure

```
.
├── main.py                      # Gradio app + OpenAI/OpenRouter client + tools
├── me.py                        # Legacy module (superseded by main.py)
├── pyproject.toml               # Python 3.11+, gradio, openai, python-dotenv
├── uv.lock                      # Locked dependency graph
├── Dockerfile                   # python:3.11-slim + uv, expose 7860
├── .dockerignore
├── .env.example                 # OPENROUTER_API_KEY
├── .github/workflows/deploy.yml # CI/CD
└── terraform/
    ├── versions.tf              # Providers, backend (local), default tags
    ├── variables.tf             # All inputs
    ├── ecr.tf                   # Container registry
    ├── iam.tf                   # Access role + instance role + secret policy
    ├── secrets.tf               # Secrets Manager secret
    ├── cloudwatch.tf            # Log group
    ├── apprunner.tf             # Service + autoscaling
    ├── outputs.tf               # ECR URL, service ARN, service URL, secret ARN
    └── terraform.tfvars.example
```

---

## Configuration reference

### Environment variables

| Var | Required | Source |
|---|---|---|
| `OPENROUTER_API_KEY` | ✅ | `.env` locally, Secrets Manager in production |
| `GRADIO_SERVER_NAME` | optional | defaults to `0.0.0.0` in Dockerfile/App Runner |
| `GRADIO_SERVER_PORT` | optional | defaults to `7860` |

### OpenAI SDK / OpenRouter wiring (in `main.py`)

```python
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ["OPENROUTER_API_KEY"],
)
MODEL = "openai/gpt-4o-mini"
```

### Tuning App Runner sizing

Edit `terraform/terraform.tfvars` (or pass `-var` on the command line):

```hcl
cpu                         = "2048"   # 2 vCPU
memory                      = "4096"   # 4 GB
autoscaling_min_size        = 2
autoscaling_max_size        = 10
autoscaling_max_concurrency = 80
```

Then `terraform apply`.
