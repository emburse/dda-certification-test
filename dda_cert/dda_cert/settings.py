import os

BASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")

# Base DDA resource endpoint
# ex. https://example.com/dda/1.0
DDA_ENDPOINT_BASE_URL = ""

# DDA spec account resource
DDA_ACCOUNT = DDA_ENDPOINT_BASE_URL + "/account"
# DDA spec account transactions resource
DDA_ACCOUNT_TRANSACTIONS = DDA_ENDPOINT_BASE_URL + "/account/transactions"
# DDA spec account transactions resource
DDA_ACCOUNTLIST = DDA_ENDPOINT_BASE_URL + "/accountlist"
# AccountsDetails resource (POST and GET)
DDA_ACCOUNTSDETAILS = DDA_ENDPOINT_BASE_URL + "/accountsdetails"

# OAuth 2.0 access token
ACCESS_TOKEN = ""

# Account ID to be used, specify it if the DDA accountId format is different from the format
# used in OFX ACCTID field
ACCOUNT_ID = ""

# Absolute path to the .ofx file containing test data
OFX_FILE_PATH = ""
