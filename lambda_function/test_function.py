import os
import boto3
import logging
from utils import get_secret
DEFAULT_TAGS = os.environ.get("DEFAULT_TAGS")
print("DEFAULT_TAGS", DEFAULT_TAGS)

logger = logging.getLogger()
level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
print("Logging level -- ", level)
logger.setLevel(level)

ec2_resource = boto3.resource('ec2')
ec2_client = boto3.client('ec2')
    
def lambda_handler(event, context):
    bucket_name = str(event["detail"]["bucket"]["name"])
    file_name = str(event["detail"]["object"]["key"])
    file_name_without_prefix = file_name.split('/')[-1]

    logger.debug(event)
    print("event -- ", event)
    
    print("secret -- ", get_secret('sharepoint_secret')['client_id'])

    scan_staus = 'Initial'
    if scan_staus == 'Initial':
        s3 = boto3.resource('s3')
        copy_source = {
            'Bucket': bucket_name,
            'Key': file_name
        }
        s3.meta.client.copy(copy_source, bucket_name, f'scan_result/{file_name_without_prefix}')
        s3.Object(bucket_name,file_name).delete()



    instances = ['i-09cafb1d617acfd93']

    if not instances:
        logger.warning('No instances available with this tags')
    else:
        if event['action'] == 'start':
            ec2_client.start_instances(InstanceIds=instances)
            logger.info('Starting instances.')
        elif event['action'] == 'stop':
            ec2_client.stop_instances(InstanceIds=instances)
            logger.info('Stopping instances.')
        else:
            logger.warning('No instances availables with this tags')