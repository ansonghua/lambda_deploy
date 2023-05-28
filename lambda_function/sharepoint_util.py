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


    if "access_token" in result:
        access_token = result['access_token']
        return access_token
    else:
        raise Exception("No Access Token found")