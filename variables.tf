variable "env" {
  default = "dev2"
}

variable "region" {
  default = "us-east-1"
}

variable "email_to" {
  default = "xxx@ccc.com"
}

variable "email_from" {
  default = "yyy@ccc.com"
}

# variable "path_source_code" {
#   default = "lambda_function"
# }

# variable "function_name" {
#   default = "aws_lambda_test"
# }

# variable "runtime" {
#   default = "python3.7"
# }

# variable "output_path" {
#   description = "Path to function's deployment package into local filesystem. eg: /path/lambda_function.zip"
#   default = "lambda_function.zip"
# }

# variable "distribution_pkg_folder" {
#   description = "Folder name to create distribution files..."
#   default = "lambda_dist_pkg"
# }

# variable "bucket_for_videos" {
#   description = "Bucket name for put videos to process..."
#   default = "aws-lambda-function-read-videos-amy"
# }
