import os
import boto3
import logging
from utils import get_secret
from sharepoint_util import get_access_token, upload_file_to_sharepoint,get_drive_id,get_sharepoint_file_path,download_file_from_sharepoint

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
    
    sharepoint_secret =  get_secret('sharepoint_secret')
    tenant_id = sharepoint_secret['tenant_id']
    app_id = sharepoint_secret['app_id']
    client_secret = sharepoint_secret['client_secret']

    scan_staus = 'Initial'
    s3 = boto3.resource('s3')
    if scan_staus == 'Initial':
        copy_source = {
            'Bucket': bucket_name,
            'Key': file_name
        }
        s3.meta.client.copy(copy_source, bucket_name, f'scan_result/{file_name_without_prefix}')

    
    access_token = get_access_token(tenant_id, app_id, client_secret)
 
    client_drive_name = sharepoint_secret['client_drive_name']
    client_site_id = sharepoint_secret['client_site_id']
    site_url_prefix = f'https://graph.microsoft.com/v1.0/sites/{client_site_id}'
    drive_id = get_drive_id(access_token,site_url_prefix, client_drive_name)
    drive_path = f'{site_url_prefix}/drives/{drive_id}/root:'

    folder_relative_path = 'Amy'
    # file_name = 'template.pptx'
    file_relative_path = f'{folder_relative_path}/{file_name_without_prefix}'
    sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)
 
    s3.Bucket(bucket_name).download_file(file_name, f'/tmp/${file_name_without_prefix}')
    upload_file_to_sharepoint(access_token, sharepoint_file_path, f'/tmp/${file_name_without_prefix}')
    # print(access_token)
    s3.Object(os.environ['REPROT_BUCKET_NAME'],file_name).delete()
#################################
    
    download_file_name = 'template.pptx'
    file_relative_path = f'{folder_relative_path}/{download_file_name}'
    sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)
    download_file_from_sharepoint(access_token, sharepoint_file_path, f'/tmp/${download_file_name}')


    s3_bucket = s3.Bucket(name=bucket_name)
    s3_bucket.upload_file(
        Filename=f'/tmp/${download_file_name}',
        Key=f'from_sp/${download_file_name}'
    )

    # instances = ['i-09cafb1d617acfd93']

    # if not instances:
    #     logger.warning('No instances available with this tags')
    # else:
    #     if event['action'] == 'stop':

    #         ec2_client.start_instances(InstanceIds=instances)
    #         logger.info('Starting instances.')
    #     # elif event['action'] == 'start':
    #     #     ec2_client.stop_instances(InstanceIds=instances)
    #     #     logger.info('Stopping instances.')
    #     else:
    #         logger.warning('No instances availables with this tags')

