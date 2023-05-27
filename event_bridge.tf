resource "aws_cloudwatch_event_rule" "s3_object_create_invoke_lambda" {

  name           = "amy-event-bridge-test-rule"
  description    = "Justification file has been posted"

  event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["Object Created"],
  "detail": {
    "bucket": {
      "name": ["${aws_s3_bucket.my_bucket.bucket}"]
    },
    "object": {
      "key": [{
        "prefix": "justifications_processed"
      }]
    }
  }
}
EOF
}

resource "aws_cloudwatch_event_target" "s3_object_create_invoke_lambda" {
  rule           = aws_cloudwatch_event_rule.s3_object_create_invoke_lambda.name
  arn            = aws_lambda_function.test_lambda.arn
}