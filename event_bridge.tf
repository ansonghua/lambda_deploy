resource "aws_cloudwatch_event_rule" "s3_object_create_invoke_lambda" {

  name           = "start_ec2"
  description    = "Invoke Lambda When Object Created"

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
        "prefix": "scan-results.json"
      }]
    }
  }
}
EOF
}

resource "aws_cloudwatch_event_rule" "s3_object_delete_invoke_lambda" {

  name           = "stop_ec2"
  description    = "Invoke lambda when Object Deleted."

  event_pattern = <<EOF
{
  "source": ["aws.s3"],
  "detail-type": ["Object Deleted"],
  "detail": {
    "bucket": {
      "name": ["${aws_s3_bucket.my_bucket.bucket}"]
    },
    "object": {
      "key": [{
        "prefix": "input"
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

resource "aws_cloudwatch_event_target" "s3_object_delete_invoke_lambda" {
  rule           = aws_cloudwatch_event_rule.s3_object_delete_invoke_lambda.name
  input          = "{\"action\":\"stop\"}"
  arn            = aws_lambda_function.test_lambda.arn
}