import json
import unittest

import requests
from ofxtools.Parser import OFXTree

from ..settings import DDA_ACCOUNT_TRANSACTIONS, OFX_FILE_PATH, ACCESS_TOKEN, ACCOUNT_ID


class TestAccounts(unittest.TestCase):

    def setUp(self):
        parser = OFXTree()
        parser.parse(OFX_FILE_PATH)

        self.ofx = parser.convert()
        self.ofx_statement = self.ofx.statements[0]
        self.ofx_transactions = self.ofx_statement.transactions
        self.auth_headers = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}

    def test_account_transactions(self):

        startTime = self.ofx_statement.banktranlist.dtstart.isoformat()
        endTime = self.ofx_statement.banktranlist.dtend.isoformat()

        r = requests.post(DDA_ACCOUNT_TRANSACTIONS, data={
            "accountId": ACCOUNT_ID,
            "startTime": startTime,
            "endTime": endTime,
        }, headers=self.auth_headers)

        result = json.loads(r.content)

        for i, transaction in enumerate(self.ofx_transactions):
            result_transaction = result["Transactions"][i]

            # Compare transaction IDs
            self.assertTrue(transaction.fitid == result_transaction["TransactionId"])

            # Verify transaction amount (+/- Decimal)
            self.assertTrue(float(transaction.trnamt) == float(result_transaction["Amount"]))

            # Verify transaction type: DEBIT, CREDIT, MEMO
            self.assertTrue(transaction.trntype == result_transaction["DebitCreditMemo"])

            # check for transaction category code (SIC/MCC)
            if transaction.sic:
                self.assertEqual(str(transaction.sic), str(result_transaction["Category"]))
