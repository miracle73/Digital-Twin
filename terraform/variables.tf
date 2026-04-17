variable "aws_region" {
  description = "AWS region for all resources."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short identifier used to name ECR repo, App Runner service, IAM roles, etc."
  type        = string
  default     = "digital-twin"
}

variable "environment" {
  description = "Environment label applied as a tag (prod, staging, dev)."
  type        = string
  default     = "prod"
}

variable "image_tag" {
  description = "ECR image tag that App Runner should deploy. CI/CD overrides this per commit."
  type        = string
  default     = "latest"
}

variable "openrouter_api_key" {
  description = "OpenRouter API key. Stored in AWS Secrets Manager; never persisted to state unencrypted."
  type        = string
  sensitive   = true
}

variable "cpu" {
  description = "App Runner vCPU allocation (in 1/1024 vCPU units). 1024 = 1 vCPU."
  type        = string
  default     = "1024"
}

variable "memory" {
  description = "App Runner memory allocation in MB. 2048 = 2 GB."
  type        = string
  default     = "2048"
}

variable "autoscaling_min_size" {
  description = "Minimum provisioned App Runner instances."
  type        = number
  default     = 1
}

variable "autoscaling_max_size" {
  description = "Maximum provisioned App Runner instances."
  type        = number
  default     = 3
}

variable "autoscaling_max_concurrency" {
  description = "Requests per instance before App Runner triggers a scale-out."
  type        = number
  default     = 100
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days."
  type        = number
  default     = 14
}

variable "container_port" {
  description = "Container port exposed by the Gradio app."
  type        = string
  default     = "7860"
}
