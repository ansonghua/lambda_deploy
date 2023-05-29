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

def split_and_upload_csp_scan_result(df,csps,bucket_name,rescan):
    for csp in csps:
        csp_scan_file_name = f'{csp}-{scan_result_file_name}'
        local_file_path = f'/tmp/{csp_scan_file_name}'
        
        check_lilst = df['query_result']['data']['rows']
        csp_cheks_list = [check for check in check_lilst if check['Provider'] == csp]
        if len(csp_cheks_list) == 0:
            continue
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
    
    rescan = True
  
    if file_name_without_prefix == scan_result_file_name:
        file_content = s3.Bucket(bucket_name).Object(file_name).get()['Body'].read()
        file_obj = io.BytesIO(file_content)
        df = pd.read_json(file_obj)
        split_and_upload_csp_scan_result(df, ['azure','aws','gcp'], bucket_name,rescan)

    if rescan:
        download_file_name = scan_result_file_name
        file_relative_path = f'{folder_relative_path}/{download_file_name}'
        sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)
        download_file_from_sharepoint(access_token, sharepoint_file_path, f'/tmp/{download_file_name}')
        df = pd.read_json(f'/tmp/{download_file_name}')
        split_and_upload_csp_scan_result(df, ['azure','aws','gcp'], bucket_name, False)
        # print(f'donwload file name: {download_file_name}')
        # s3_bucket = s3.Bucket(name=bucket_name)
        # s3_bucket.upload_file(
        #     Filename=f'/tmp/{download_file_name}',
        #     Key=f'from_sp/{download_file_name}'
        # )

#     scan_staus = 'Initial'

#     if scan_staus == 'Initial':
#         copy_source = {
#             'Bucket': bucket_name,
#             'Key': file_name
#         }
#         s3.meta.client.copy(copy_source, bucket_name, f'scan_result/{file_name_without_prefix}')

    

    if rescan:
        file_name_without_prefix = file_name_without_prefix.replace('scan','rescan')
    file_relative_path = f'{folder_relative_path}/{file_name_without_prefix}'
    sharepoint_file_path = get_sharepoint_file_path(drive_path,file_relative_path)

    s3.Bucket(bucket_name).download_file(file_name, f'/tmp/{file_name_without_prefix}')
    upload_file_to_sharepoint(access_token, sharepoint_file_path, f'/tmp/{file_name_without_prefix}')
    # print(access_token)
    s3.Object(os.environ['REPROT_BUCKET_NAME'],file_name).delete()
# #################################
    

#################################
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

