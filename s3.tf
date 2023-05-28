resource "aws_s3_bucket" "my_bucket" {
  bucket = "amy-test-${var.env}"
}

resource "aws_s3_bucket_server_side_encryption_configuration" "my_bucket" {
  bucket = aws_s3_bucket.my_bucket.bucket

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.my_bucket_kms_key.arn
      sse_algorithm     = "aws:kms"
    }
  }
}

resource "aws_s3_bucket_notification" "my_bucket" {
  bucket = aws_s3_bucket.my_bucket.bucket
  eventbridge = true
}


resource "aws_s3_bucket_public_access_block" "my_bucket" {
  bucket = aws_s3_bucket.my_bucket.bucket

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

# resource "aws_s3_bucket_versioning" "bucket" {
#   bucket = aws_s3_bucket.my_bucket.bucket
#   versioning_configuration {
#     status = "Enabled"
#   }
# }

# resource "aws_s3_bucket_acl" "bucket" {
#   bucket = aws_s3_bucket.my_bucket.bucket
#   acl    = "private"
# }