resource "aws_apprunner_auto_scaling_configuration_version" "app" {
  auto_scaling_configuration_name = var.project_name

  min_size        = var.autoscaling_min_size
  max_size        = var.autoscaling_max_size
  max_concurrency = var.autoscaling_max_concurrency

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_apprunner_service" "app" {
  service_name = var.project_name

  source_configuration {
    auto_deployments_enabled = false

    authentication_configuration {
      access_role_arn = aws_iam_role.apprunner_ecr_access.arn
    }

    image_repository {
      image_identifier      = "${aws_ecr_repository.app.repository_url}:${var.image_tag}"
      image_repository_type = "ECR"

      image_configuration {
        port = var.container_port

        runtime_environment_variables = {
          GRADIO_SERVER_NAME       = "0.0.0.0"
          GRADIO_SERVER_PORT       = var.container_port
          GRADIO_ANALYTICS_ENABLED = "False"
        }

        runtime_environment_secrets = {
          OPENROUTER_API_KEY = aws_secretsmanager_secret.openrouter_api_key.arn
        }
      }
    }
  }

  instance_configuration {
    cpu               = var.cpu
    memory            = var.memory
    instance_role_arn = aws_iam_role.apprunner_instance.arn
  }

  auto_scaling_configuration_arn = aws_apprunner_auto_scaling_configuration_version.app.arn

  health_check_configuration {
    protocol            = "TCP"
    interval            = 10
    timeout             = 5
    healthy_threshold   = 1
    unhealthy_threshold = 5
  }

  depends_on = [
    aws_iam_role_policy_attachment.apprunner_ecr_access,
    aws_iam_role_policy_attachment.apprunner_instance_secrets,
    aws_secretsmanager_secret_version.openrouter_api_key,
  ]
}
