import os

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

# Base DDA resource endpoint
# ex. https://example.com/dda/1.0
DDA_ENDPOINT_BASE_URL = ""

# DDA spec account resource
DDA_ACCOUNT = DDA_ENDPOINT_BASE_URL + "/account"
# DDA spec: Get a lightweight list of accounts for the current token.
DDA_ACCOUNT_LIST = DDA_ENDPOINT_BASE_URL + "/accountlist"
# DDA spec account transactions resource
DDA_ACCOUNT_TRANSACTIONS = DDA_ENDPOINT_BASE_URL + "/account/transactions"
# AccountsDetails resource (POST and GET)
DDA_ACCOUNTSDETAILS = DDA_ENDPOINT_BASE_URL + "/accountsdetails"

# OAuth 2.0 access token
ACCESS_TOKEN = ""

# Absolute path to the .ofx file containing test data
OFX_FILE_PATH = ""
