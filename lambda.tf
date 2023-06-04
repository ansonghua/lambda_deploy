data "archive_file" "test_zip" {
  type        = "zip"
  source_dir = "${path.module}/lambda_function"
  output_path = "${path.module}/myzip/test.zip"
}

resource "aws_lambda_function" "test_lambda" {
  filename      = "${path.module}/myzip/test.zip"
  source_code_hash = data.archive_file.test_zip.output_base64sha256
  function_name = "test_function"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "test_function.lambda_handler"
  runtime       = "python3.9"
  timeout       = 600
  memory_size   = 192

  layers = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:3"]

  environment {
    variables = {
      aws_region = var.region
      EMAIL_TO       = var.email_to
      EMAIL_FROM       = var.email_from
      CONFIG_SECRET_ARN       = aws_secretsmanager_secret.my_secret.arn
      BUCKET_NAME             = aws_s3_bucket.my_bucket.bucket
      REPROT_BUCKET_NAME      = aws_s3_bucket.my_bucket.bucket
    }
  }
  # lifecycle {
  #   ignore_changes = [source_code_hash]
  # }
}

resource "aws_lambda_permission" "object_created_invoke_lambda" {
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "events.amazonaws.com"
  action        = "lambda:InvokeFunction"
  statement_id  = "AllowExecutionFromObjectedAddedEvent"
  source_arn    = aws_cloudwatch_event_rule.s3_object_create_invoke_lambda.arn
}

resource "aws_lambda_permission" "objecte_deleted_invoke_lambda" {
  function_name = aws_lambda_function.test_lambda.function_name
  principal     = "events.amazonaws.com"
  action        = "lambda:InvokeFunction"
  statement_id  = "AllowExecutionFromObjectedDeletedEvent"
  source_arn    = aws_cloudwatch_event_rule.s3_object_delete_invoke_lambda.arn
}

#########################
data "archive_file" "justification_zip" {
  type        = "zip"
  source_dir = "${path.module}/lambda_function"
  output_path = "${path.module}/myzip/justification_lambda.zip"
}

resource "aws_lambda_function" "justification_lambda" {
  filename      = "${path.module}/myzip/justification_lambda.zip"
  source_code_hash = data.archive_file.justification_zip.output_base64sha256
  function_name = "justification_lambda"
  role          = aws_iam_role.lambda_exec_role.arn
  handler       = "justification_lambda.lambda_handler"
  runtime       = "python3.9"
  timeout       = 600
  memory_size   = 192

  layers = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python39:3"]

  environment {
    variables = {
      aws_region = var.region
      EMAIL_TO       = var.email_to
      EMAIL_FROM       = var.email_from
      CONFIG_SECRET_ARN       = aws_secretsmanager_secret.my_secret.arn
      BUCKET_NAME             = aws_s3_bucket.my_bucket.bucket
      REPROT_BUCKET_NAME      = aws_s3_bucket.my_bucket.bucket
    }
  }
  lifecycle {
    ignore_changes = [source_code_hash]
  }
}

resource "aws_lambda_permission" "object_created_invoke_justification_lambda" {
  function_name = aws_lambda_function.justification_lambda.function_name
  principal     = "events.amazonaws.com"
  action        = "lambda:InvokeFunction"
  statement_id  = "AllowExecutionFromObjectedAddedEvent"
  source_arn    = aws_cloudwatch_event_rule.s3_object_create_invoke_jsutification_lambda.arn
}
