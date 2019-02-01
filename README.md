# dda-certification-test
DDA Certification Test Suite is designed to help developers certify their DDA-compliant APIs.
This test suite provides a set of tests to ensure data consistency and compatibility
with DDA requirements.

Currently, the DDA v1.0 spec is covered by this test suite.

## Requirements
1. An OFX file is required to validate data returned from the Bank Transaction List endpoint. The contents of an example OFX file is shown below:

    ```XML
    <?xml version="1.0" encoding="US-ASCII"?>
    <?OFX OFXHEADER="200" VERSION="211" SECURITY="NONE" OLDFILEUID="NONE" NEWFILEUID="NONE"?>
    <OFX>
      <SIGNONMSGSRSV1>
        <SONRS>
          <STATUS>
            <CODE>0</CODE>
            <SEVERITY>INFO</SEVERITY>
          </STATUS>
          <DTSERVER>20190130</DTSERVER>
          <LANGUAGE>ENG</LANGUAGE>
        </SONRS>
      </SIGNONMSGSRSV1>
      <BANKMSGSRSV1>
        <STMTTRNRS>
          <TRNUID>0</TRNUID>
          <STATUS>
            <CODE>0</CODE>
            <SEVERITY>INFO</SEVERITY>
          </STATUS>
          <STMTRS>
            <CURDEF>USD</CURDEF>
            <BANKACCTFROM>
              <BANKID>000000000</BANKID>
              <ACCTID>100000000000</ACCTID>
              <ACCTTYPE>CHECKING</ACCTTYPE>
            </BANKACCTFROM>
            <BANKTRANLIST>
              <DTSTART>20180301</DTSTART>
              <DTEND>20190130</DTEND>

              <STMTTRN>
                <TRNTYPE>CREDIT</TRNTYPE>
                <DTPOSTED>20190120</DTPOSTED>
                <TRNAMT>10000.00</TRNAMT>
                <FITID>00000000-0000-0000-0000-000000000001</FITID>
                <NAME>1: Transfer</NAME>
              </STMTTRN>

              <STMTTRN>
                <TRNTYPE>DEBIT</TRNTYPE>
                <DTPOSTED>20190120</DTPOSTED>
                <TRNAMT>-15.32</TRNAMT>
                <FITID>00000000-0000-0000-0000-000000000002</FITID>
                <SIC>0000</SIC>
                <NAME>2: Test</NAME>
                <MEMO>Test transaction</MEMO>
              </STMTTRN>
            </BANKTRANLIST>
            <LEDGERBAL>
              <BALAMT>10000.00</BALAMT>
              <DTASOF>20190130</DTASOF>
            </LEDGERBAL>
          </STMTRS>
        </STMTTRNRS>
      </BANKMSGSRSV1>
    </OFX>
    ```

2. An OAuth 2.0 Access Token is required for making requests to DDA endpoints. This certification test suite does not test the OAuth token issuance process, and instead assumes that a valid token has already been retrieved for use in the `Authorization: Bearer ACCESS_TOKEN` Header.

## Installation instructions
This certification test suite is implemented using Python and depends upon requirements defined within `requirements.txt`. We recommend creating a virtualenv to avoid polluting your the global environment with Python requirements:
```
virtualenv .venv --no-site-packages
```
Activate the virtual Python environment and install Python requirements:
```
source ./.venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Configuration
Open `dda-certification-test/dda_cert/settings.py` file and configure the following required fields:

```
DDA_ENDPOINT_BASE_URL = "https://example.com/dda/1.0"

# OAuth 2.0 access token
ACCESS_TOKEN = "0000000000000000000000000000000000000000"

# Absolute path to the .ofx file containing test data
OFX_FILE_PATH = os.path.join(BASE_PATH, "statement-2018-03-01.ofx")
```
Please note that the OFX_FILE_PATH is relative to the `dda-certification-test` directory.

# Testing
Simply run:
```
cd dda-certification-test
python -m unittest dda_cert.tests
```