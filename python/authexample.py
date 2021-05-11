#!/usr/bin/env python3

import requests
import json
import os
import logging

logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

client_id = os.environ.get("API_CLIENT_ID")
client_secret = os.environ.get("API_CLIENT_SECRET")
scope = os.environ.get("API_SCOPE")

if client_id is None or client_secret is None or scope is None:
    logging.error("Invalid API credentials.")
    quit()

logging.info("API credentials successfully set [client_id=%s]" %client_id)

# The API authentication endpoint
authURL = 'https://login.microsoftonline.com/efa98c7b-2114-46e8-be99-954a4f1a2d9c/oauth2/v2.0/token'

# Authenticate to the endpoint and get the token

postBody = {
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope,
    'grant_type': 'client_credentials'
}

# Send the authentication request...
resp = requests.post(authURL, data=postBody)

if resp.status_code != 200:
    logging.error("Request failed [%s]" % resp.text)
    quit()

jsonbody = json.loads(resp.text)
token = jsonbody["access_token"]

logging.info("Successfully retrieved access token [%s]" % jsonbody["token_type"])

authHeader = {"Authorization": "Bearer %s" %
              token, 'User-Agent': 'ProposedPriceExtract'}

# The Data API endpoint
priceEndpoint = 'https://dev.data.thekalibratecloud.com/api/price'

# Proposed Price Query
# Note that the exportedTime will need to be updated each time. This is jsut an example.
query = "(entityVariant=Proposed)+(status.exported=true)+(exportedTime>=2020-06-01)+(orderBy=exportedTime)+(direction=descending)"

queryURL = priceEndpoint + "?query=" + query
response = requests.get(queryURL, headers=authHeader, timeout=60)

if response.status_code != 200:
    logging.error("API Request failed [%s]" % response.text)
    quit()

logging.info("Successfully executed query [%s]" % queryURL)

rawdata = json.loads(response.text)

logging.info(rawdata)