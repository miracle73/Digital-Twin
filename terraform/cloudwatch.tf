# App Runner auto-provisions CloudWatch log groups named
# /aws/apprunner/<service>/<service-id>/application and .../service.
# This log group is an additional application-level group the service can
# write structured logs to (via aws-sdk in code, or via log router integration).
resource "aws_cloudwatch_log_group" "app" {
  name              = "/aws/apprunner/${var.project_name}/application"
  retention_in_days = var.log_retention_days
}
