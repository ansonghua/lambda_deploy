import os
import io
import boto3
import logging
from utils import get_secret
from sharepoint_util import get_access_token, upload_file_to_sharepoint,get_drive_id,get_sharepoint_file_path,download_file_from_sharepoint
import pandas as pd

DEFAULT_TAGS = os.environ.get("DEFAULT_TAGS")
print("DEFAULT_TAGS", DEFAULT_TAGS)

logger = logging.getLogger()
level = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))
print("Logging level -- ", level)
logger.setLevel(level)

# ec2_resource = boto3.resource('ec2')
# ec2_client = boto3.client('ec2')

scan_result_file_name = 'scan-results.json'

s3 = boto3.resource('s3')

def split_and_upload_csp_scan_result(df,csp,bucket_name,rescan):

    
    csp_scan_file_name = f'{csp}-{scan_result_file_name}'
    local_file_path = f'/tmp/{csp_scan_file_name}'
    
    check_lilst = df['query_result']['data']['rows']
    csp_cheks_list = [check for check in check_lilst if check['Provider'] == csp]
    print(f'{csp} csp_cheks_list length:---> {len(csp_cheks_list)}')
    if len(csp_cheks_list) == 0:
        return

    df['query_result']['data']['rows'] = csp_cheks_list
    df.to_json(local_file_path)
    
    s3_bucket = s3.Bucket(name=bucket_name)
    file_prefix = "rescan" if rescan else "initial-scan"
    s3_bucket.upload_file(
        Filename= local_file_path,
        Key=f'{file_prefix}/{csp_scan_file_name}'
    )

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
    access_token = get_access_token(tenant_id, app_id, client_secret)

    client_drive_name = sharepoint_secret['client_drive_name']
    client_site_id = sharepoint_secret['client_site_id']
    site_url_prefix = f'https://graph.microsoft.com/v1.0/sites/{client_site_id}'
    drive_id = get_drive_id(access_token,site_url_prefix, client_drive_name)
    drive_path = f'{site_url_prefix}/drives/{drive_id}/root:'

    folder_relative_path = 'Amy'

    download_file_name = 'justifications.csv'
    file_relative_path = f'{folder_relative_path}/{download_file_name}'
    sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)
    download_file_from_sharepoint(access_token, sharepoint_file_path, f'/tmp/{download_file_name}')




# parquet, add client info in file name
    s3_bucket = s3.Bucket(name=bucket_name)
    s3_bucket.upload_file(
        Filename= f'/tmp/{download_file_name}',
        Key=f'processed_justifications/justifications.parquet'
    )
# CSV
    file_relative_path = f'{folder_relative_path}/processed_{download_file_name}'
    sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)
    upload_file_to_sharepoint(access_token, sharepoint_file_path, f'/tmp/{download_file_name}')






  