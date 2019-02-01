import json
import unittest
from urllib.parse import urlencode

import requests
from ofxtools.Parser import OFXTree

from ..settings import DDA_ACCOUNT_TRANSACTIONS, OFX_FILE_PATH, ACCESS_TOKEN, DDA_ACCOUNT_LIST, \
    DDA_ACCOUNT


class TestAccounts(unittest.TestCase):

    def setUp(self):
        parser = OFXTree()
        parser.parse(OFX_FILE_PATH)
        self.ofx = parser.convert()
        self.auth_headers = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}
        self.accounts_map = {}

    def __get_accounts_map(self):
        """
        Fetch the map of accounts represented by account numbers
        """

        # get the list of available accounts
        request = requests.get(DDA_ACCOUNT_LIST, headers=self.auth_headers)
        result = json.loads(request.content)

        accounts_by_acc_number = {}
        for account_descriptor in result.get("AccountDescriptorList"):
            response = requests.post(
                DDA_ACCOUNT,
                headers={**self.auth_headers, "Content-Type": "application/x-www-form-urlencoded"},
                data=urlencode({
                    "accountId": str(account_descriptor["AccountId"]),
                })
            )
            content = json.loads(response.content)

            # get the first key (ofe of the account types)
            account = content[list(content.keys())[0]]

            # assign to the account number
            accounts_by_acc_number[account["AccountNumber"]] = account

        return accounts_by_acc_number

    def test_account_list_pagination(self):
        """
        Tests (13.4.) Accounts Entity - An optionally paginated array of accounts.
        """
        pass

    def test_account_list(self):
        request = requests.get(DDA_ACCOUNT_LIST, headers=self.auth_headers)
        result = json.loads(request.content)

        self.assertTrue("AccountDescriptorList" in result.keys(),
                        "AccountDescriptorList was not found in the /accountlist response body.")

        # Iterate through all account descriptors returned by the DDA endpoint,
        # verify that all required fields are provided
        for account in result.get("AccountDescriptorList"):
            # Long-term persistent identity of the account. Not an account number.
            # This identity must be unique to the owning institution.
            self.assertTrue("AccountId" in account.keys(),
                            "AccountId which is a required key was not found in AccountDescriptor entity.")

            # Account identity to display to customer. This may be a masked account number or product name
            # followed by masked number.
            self.assertTrue("DisplayName" in account.keys(),
                            "DisplayName which is a required key was not found in AccountDescriptor entity.")

            # Account status
            self.assertTrue("Status" in account.keys(),
                            "Status which is a required key was not found in AccountDescriptor object.")
            VALID_ACCOUNT_STATUSES = ["OPEN", "CLOSED", "PENDINGOPEN", "PENDINGCLOSE", "DELINQUENT", "PAID",
                                      "NEGATIVECURRENTBALANCE", ]
            self.assertTrue(account["Status"] in VALID_ACCOUNT_STATUSES,
                            "Account Status it not one if the valid values: {}".format(VALID_ACCOUNT_STATUSES))

    def test_account(self):
        """
        12.1. POST /account

        Get an account.

        Request Formats
            application/x-www-form-urlencoded

        Response Formats
            application/json, application/xml

        Response
            one of DepositAccount, LoanAccount, LocAccount, or InvestmentAccount

        This test checks whether all required fields are properly transmitted,
        AccountDescriptor and Account entities are taken into consideration.

        Because OFX files might not contain AccountId fields (needed to query account details),
        but AccountNumber instead, we have to go through all accounts and search for corresponding
        AccountIds.
        """

        VALID_ACCOUNT_TYPES = ["DepositAccount", "LoanAccount", "LocAccount", "InvestmentAccount"]

        # get the list of available accounts
        request = requests.get(DDA_ACCOUNT_LIST, headers=self.auth_headers)
        result = json.loads(request.content)

        accounts_by_acc_number = {}
        for account_descriptor in result.get("AccountDescriptorList"):
            response = requests.post(
                DDA_ACCOUNT,
                headers={**self.auth_headers, "Content-Type": "application/x-www-form-urlencoded"},
                data=urlencode({
                    "accountId": str(account_descriptor["AccountId"]),
                })
            )
            content = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(content) > 0)

            # get common elements of both lists, produces a set
            account_descriptor = VALID_ACCOUNT_TYPES & content.keys()

            # check whether returned account type is valid, empty set means that none of the valid
            # choices was returned
            self.assertTrue(bool(account_descriptor))

            # account type is valid and present, pull it from the response content
            account_type = account_descriptor.pop()

            account = content[account_type]

            # Long-term persistent identity of the account. Not an account number.
            # This identity must be unique to the owning institution.
            self.assertTrue("AccountId" in account.keys(),
                            "AccountId which is a required key was not found in AccountDescriptor entity.")

            # Account identity to display to customer. This may be a masked account number or product name
            # followed by masked number.
            self.assertTrue("DisplayName" in account.keys(),
                            "DisplayName which is a required key was not found in AccountDescriptor entity.")

            # Account status
            self.assertTrue("Status" in account.keys(),
                            "Status which is a required key was not found in AccountDescriptor entity.")
            VALID_ACCOUNT_STATUSES = ["OPEN", "CLOSED", "PENDINGOPEN", "PENDINGCLOSE", "DELINQUENT", "PAID",
                                      "NEGATIVECURRENTBALANCE", ]
            self.assertTrue(account["Status"] in VALID_ACCOUNT_STATUSES,
                            "Account Status it not one if the valid values: {}".format(VALID_ACCOUNT_STATUSES))

            # Currency Aggregate
            self.assertTrue("Currency" in account.keys(),
                            "Currency which is a required key was not found in the Account entity.")

            # End user’s handle for account at owning institution
            self.assertTrue("AccountNumber" in account.keys(),
                            "AccountNumber which is a required key was not found in the Account entity.")

            # Interest Rate of Account
            self.assertTrue("InterestRate" in account.keys(),
                            "InterestRate which is a required key was not found in the Account entity.")

            # As-of date of balances - required
            self.assertTrue("BalanceAsOf" in account.keys(),
                            "BalanceAsOf which is a required key was not found in DepositAccount entity.")

            # Balance of funds in account - required
            self.assertTrue("CurrentBalance" in account.keys(),
                            "CurrentBalance which is a required key was not found in DepositAccount entity.")

            # if all is valid, add the account to map
            accounts_by_acc_number[account["AccountNumber"]] = account

        accounts_from_ofx = [statement.account for statement in self.ofx.statements]
        account_numbers_from_ofx = [statement.account.acctid for statement in self.ofx.statements]

        # check whether there are any accounts in one endpoint (DDA) not present in the another (OFX)
        accounts_xor = accounts_by_acc_number.keys() ^ account_numbers_from_ofx
        self.assertFalse(bool(accounts_xor),
                         "There are differences in account numbers returned by DDA and those "
                         "present in OFX file: {}.".format(", ".join(accounts_xor)))

        # check account types between OFX and DDA
        for ofx_account in accounts_from_ofx:
            self.assertEqual(ofx_account.accttype, accounts_by_acc_number[ofx_account.acctid]["AccountType"])

    def test_accountsdetails_meta(self):
        """
        12.6. GET /accountsdetails

        Get all account information (details & transactions) for the current token.

        Response Formats:
            application/json, application/xml

        Response Type:
            Accounts
        """

        accounts_map = self.__get_accounts_map()

        for statement in self.ofx.statements:
            self.assertTrue(statement.account.acctid in accounts_map.keys())
            self.assertEqual(statement.account.accttype, accounts_map[statement.account.acctid]["AccountType"])

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

        accounts_map = self.__get_accounts_map()

        accountId = accounts_map[statement.account.acctid]["AccountId"]
        startTime = statement.banktranlist.dtstart.isoformat()
        endTime = statement.banktranlist.dtend.isoformat()

        r = requests.post(DDA_ACCOUNT_TRANSACTIONS, data={
            "accountId": accountId,
            "startTime": startTime,
            "endTime": endTime,
        }, headers=self.auth_headers)

        result = json.loads(r.content)
        dda_transactions = result.get("Transactions")

        # build a complete list of transactions (spanned across multiple pages)
        if result.get("TotalPages") > 1:
            for page_number in range(result.get("TotalPages") - 1):
                r = requests.post(DDA_ACCOUNT_TRANSACTIONS, data={
                    "accountId": accountId,
                    "startTime": startTime,
                    "endTime": endTime,
                    "page": page_number + 2,  # +2 to start index from 1 and add one page on top of 1
                }, headers=self.auth_headers)

                result = json.loads(r.content)
                dda_transactions += result.get("Transactions")

        # check if number of transactions is the same on both ends
        self.assertEqual(len(statement.transactions), len(dda_transactions))

        for i, transaction in enumerate(statement.transactions):
            result_transaction = dda_transactions[i]

            # Compare transaction IDs
            self.assertTrue(transaction.fitid == result_transaction["TransactionId"])

            # Verify transaction amounts, convert amount from .ofx file to positive because
            # DDA API returns positive values as well
            self.assertTrue(abs(float(transaction.trnamt)) == float(result_transaction["Amount"]))

            # Verify transaction type: DEBIT, CREDIT, MEMO
            self.assertTrue(transaction.trntype == result_transaction["DebitCreditMemo"])

            # check for transaction category code (SIC/MCC)
            if transaction.sic:
                self.assertEqual(str(transaction.sic), str(result_transaction["Category"]))
