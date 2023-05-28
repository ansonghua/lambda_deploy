import requests 
import json
from msal import ConfidentialClientApplication
import os

def get_access_token(tenant_id, app_id, client_secret):
    msal_authority= f'https://login.microsoftonline.com/{tenant_id}'
    msal_scope = ['https://graph.microsoft.com/.default']
    msal_app = ConfidentialClientApplication(
        client_id=app_id, 
        client_credential=client_secret,
        authority=msal_authority
    )

    result = msal_app.acquire_token_silent(
        scopes=msal_scope,
        account=None,
    )


    if not result:
        result = msal_app.acquire_token_for_client(msal_scope)

    # print(result)
    if "access_token" in result:
        access_token = result['access_token']
        return access_token
    else:
        raise Exception("No Access Token found")


def upload_file_to_sharepoint(access_token, upload_url, src_file_path):

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/octet-stream',
        'Content-Length': str(os.path.getsize(src_file_path))
    }
    with open(src_file_path, 'rb') as file:
        response = requests.put(upload_url, headers=headers, data=file)
        print(response.json())

def get_sharepoint_file_path(drive_path, file_relative_path):
    return f'{drive_path}/{file_relative_path}:/content'

def get_drive_id(access_token, site_url_prefix, drive_name):
    query_url= f'{site_url_prefix}/drives?$select=id,name'
    drive_list = get_list(access_token, query_url)
    for drive in drive_list:
        if drive['name'] == drive_name:
            return drive['id']

def get_list(access_token, share_point_query_url):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(   
        url= share_point_query_url,
        headers = headers,
    )
    
    return response.json()['value']



def download_file_from_sharepoint(access_token, download_url, dest_file_path):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
#     local_filename = download_url.split('/')[-2]
    print(dest_file_path)
    # NOTE the stream=True parameter below
    with requests.get(download_url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(dest_file_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk: 
                f.write(chunk)
    return dest_file_path