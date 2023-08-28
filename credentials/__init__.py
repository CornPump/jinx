# To use oauth_secret and account_secret, create two python source files and add the following reddit credentials
# Remove switch config to oauth_secret and account_secret
# Remove importing of config in oauth_secret and account_secret
from credentials.config import REDDIT_OAUTH_ID,REDDIT_OAUTH_PW
from credentials.config import REDDIT_ID,REDDIT_PW
import requests
import time

TOKEN_ACCESS_ENDPOINT = 'https://www.reddit.com/api/v1/access_token'

def create_access_token():

    # Reddit authentication data
    client_auth = requests.auth.HTTPBasicAuth(REDDIT_OAUTH_ID, REDDIT_OAUTH_PW)
    account = {'grant_type': 'password', 'username': REDDIT_ID, 'password': REDDIT_PW}
    headers = {'User-Agent': 'Comment read automation'}

    # getting Reddit's access token
    access_token = (requests.post(TOKEN_ACCESS_ENDPOINT, data=account,
                    headers=headers, auth=client_auth).json())#['access_token']
    # expires 1 hour before real expiration to give an advance of half hour
    access_token = {'key': access_token['access_token'],
                    'expires_in':int(time.time()) + int(access_token['expires_in']) - (60*30)}
    return access_token