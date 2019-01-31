# dda-certification-test
DDA Certification Test Suite was designed to help developers create their own DDA
compliant APIs.
It provides a set of tests to ensure data consistency and compatibility
with DDA requirements.

At the current moment DDA v1.0 spec is covered.

## Requirements
1. An OFX file will be needed, it has to cover Bank Transaction List, an example code is shown below:

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

2. An Access Token, DDA endpoints use OAuth 2.0, the authentication has to be done thru `Authorization: Bearer ACCESS_TOKEN` Header

## Installation instructions
It's better to use virtualenv so we don't pollute the global environment with requirements:
```
virtualenv .venv --no-site-packages
```
Activate the environment and install requiremenmts:
```
source ./.venv/bin/activate
pip install --upgrade -r requirements.txt
```

## Configuration
Open `dda-certification-test/dda_cert/dda_cert/settings.py` file and configure required fields:

```
DDA_ENDPOINT_BASE_URL = "https://example.com/dda/1.0"

# OAuth 2.0 access token
ACCESS_TOKEN = "0000000000000000000000000000000000000000"

# Absolute path to the .ofx file containing test data
OFX_FILE_PATH = os.path.join(BASE_PATH, "../statement-2018-03-01.ofx")
```
Please note that OFX_FILE_PATH is relative to the `dda-certification-test` directory.

# Testing
Simply run:
```
cd dda-certification-test
python -m unittest dda_cert.dda_cert.tests
```