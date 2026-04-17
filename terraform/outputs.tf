output "ecr_repository_url" {
  description = "Full ECR repository URL. Used by CI/CD to push built images."
  value       = aws_ecr_repository.app.repository_url
}

output "ecr_repository_name" {
  description = "ECR repository name."
  value       = aws_ecr_repository.app.name
}

output "apprunner_service_arn" {
  description = "ARN of the App Runner service. Add this to the GitHub secret APP_RUNNER_SERVICE_ARN."
  value       = aws_apprunner_service.app.arn
}

output "apprunner_service_url" {
  description = "Public HTTPS URL of the deployed App Runner service."
  value       = "https://${aws_apprunner_service.app.service_url}"
}

output "apprunner_service_id" {
  description = "App Runner service ID."
  value       = aws_apprunner_service.app.service_id
}

output "secret_arn" {
  description = "ARN of the OpenRouter API key secret."
  value       = aws_secretsmanager_secret.openrouter_api_key.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group name for application logs."
  value       = aws_cloudwatch_log_group.app.name
}
