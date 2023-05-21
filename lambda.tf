# resource "null_resource" "install_python_dependencies" {
#   provisioner "local-exec" {
#     command = "bash ${path.module}/scripts/create_pkg.sh"

#     environment = {
#       source_code_path = var.path_source_code
#       function_name = var.function_name
#       path_module = path.module
#       runtime = var.runtime
#       path_cwd = path.cwd
#     }
#   }
# }

# resource "null_resource" "install_dependencies" {
#   provisioner "local-exec" {
#     command = "pip install -r ${var.lambda_root}/requirements.txt -t ${var.lambda_root}/"
#   }
  
#   triggers = {
#     dependencies_versions = filemd5("${var.lambda_root}/requirements.txt")
#     source_versions = filemd5("${var.lambda_root}/function.py")
#   }
# }
# data "archive_file" "create_dist_pkg" {
#   depends_on = [null_resource.install_python_dependencies]
#   source_dir = "${path.cwd}/lambda_dist_pkg/"
#   output_path = var.output_path
#   type = "zip"
# }

# resource "aws_lambda_function" "aws_lambda_test" {
#   depends_on = [null_resource.install_python_dependencies]
#   function_name = var.function_name
#   description = "Process video and does face recognition..."
#   handler = "lambda_function.lambda.lambda_handler"
#   runtime = var.runtime

#   role = aws_iam_role.lambda_exec_role.arn
#   memory_size = 128
#   timeout = 300

#   source_code_hash = data.archive_file.create_dist_pkg.output_base64sha256
#   filename = data.archive_file.create_dist_pkg.output_path
# }

resource "aws_lambda_function" "aws_lambda_test" {
  s3_bucket = "amy-lambda-deployment"
  s3_key    = "lambda.zip"
  function_name    = "test-lambda"
  handler          = "module.handler"
  runtime          = "python3.9"
  timeout          = 180
  role = aws_iam_role.lambda_exec_role.arn
  memory_size = 128
}

resource "aws_lambda_permission" "allow_bucket" {
  function_name = aws_lambda_function.aws_lambda_test.arn
  source_arn = aws_s3_bucket.bucket_read_videos.arn
  statement_id = "AllowExecutionFromS3Bucket"
  action = "lambda:InvokeFunction"
  principal = "s3.amazonaws.com"
}
