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

    print(result)
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