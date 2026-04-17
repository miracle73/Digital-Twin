resource "aws_secretsmanager_secret" "openrouter_api_key" {
  name                    = "${var.project_name}/openrouter-api-key"
  description             = "OpenRouter API key consumed by the App Runner service as OPENROUTER_API_KEY."
  recovery_window_in_days = 7
}

resource "aws_secretsmanager_secret_version" "openrouter_api_key" {
  secret_id     = aws_secretsmanager_secret.openrouter_api_key.id
  secret_string = var.openrouter_api_key
}
