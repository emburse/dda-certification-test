import json
import unittest

import requests
from ofxtools.Parser import OFXTree

from ..settings import DDA_ACCOUNT_TRANSACTIONS, OFX_FILE_PATH, ACCESS_TOKEN, DDA_ACCOUNTSDETAILS


class TestAccounts(unittest.TestCase):

    def setUp(self):
        parser = OFXTree()
        parser.parse(OFX_FILE_PATH)

        self.ofx = parser.convert()
        self.auth_headers = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}

        request = requests.get(DDA_ACCOUNTSDETAILS, headers=self.auth_headers)
        result = json.loads(request.content)
        self.dda_accounts = result.get("Accounts")

        self.accounts_map = {}
        for account in self.dda_accounts:
            self.accounts_map[account["AccountNumber"]] = account

    def test_accountsdetails_meta(self):
        """
        12.6. GET /accountsdetails

        Get all account information (details & transactions) for the current token.

        Response Formats:
            application/json, application/xml

        Response Type:
            Accounts
        """

        for statement in self.ofx.statements:
            self.assertTrue(statement.account.acctid in self.accounts_map.keys())
            self.assertEqual(statement.account.accttype, self.accounts_map[statement.account.acctid]["AccountType"])

    def test_accounts_transactions(self):
        """
        Test transaction list returned by the /accountsdetails resource.
        """
        for statement in self.ofx.statements:
            self.__test_account_transactions(statement=statement)

    def __test_account_transactions(self, statement):
        """
        Test transaction listing for given account
        """

        accountId = self.accounts_map[statement.account.acctid]["AccountId"]
        startTime = statement.banktranlist.dtstart.isoformat()
        endTime = statement.banktranlist.dtend.isoformat()

        r = requests.post(DDA_ACCOUNT_TRANSACTIONS, data={
            "accountId": accountId,
            "startTime": startTime,
            "endTime": endTime,
        }, headers=self.auth_headers)

        result = json.loads(r.content)

        self.assertEqual(len(statement.transactions), len(result.get("Transactions")))
        for i, transaction in enumerate(statement.transactions):
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
