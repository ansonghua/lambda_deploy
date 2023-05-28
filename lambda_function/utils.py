import json
import os
import boto3
from botocore.exceptions import ClientError


def get_secret(secret_name):
    result = ''
    region = os.environ['aws_region']

    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region,
    )
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )

    except ClientError as cli_err:
        print(f"Client Errors: {cli_err} ")
    except Exception as exception:
        print(f'Failed to get Secret from Secret Manager: {str(exception)}')
        
    else:
        if 'SecretString' in get_secret_value_response:
            result = get_secret_value_response['SecretString']

    return json.loads(result)