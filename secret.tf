resource "aws_secretsmanager_secret" "my_secret" {
  name       = "my-app/secrets"
  kms_key_id = aws_kms_key.my_secret_kms_key.id
}