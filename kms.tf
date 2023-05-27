resource "aws_kms_key" "my_bucket_kms_key" {
  description         = "S3 Bucket Key"
  enable_key_rotation = true
}

resource "aws_kms_key" "my_secret_kms_key" {
  description         = "Secret Manager KMS Key"
  enable_key_rotation = true
}