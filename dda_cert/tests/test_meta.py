import json
import unittest

import requests
from ofxtools.Parser import OFXTree

from ..settings import DDA_ACCOUNT_TRANSACTIONS, OFX_FILE_PATH, ACCESS_TOKEN, DDA_ACCOUNTSDETAILS


class TestMeta(unittest.TestCase):

    def setUp(self):
        pass

    def test_connection(self):
        pass

    def test_dda_interactionid(self):
        pass

    def test_authorization(self):
        self.auth_headers = {"Authorization": "Bearer {}".format(ACCESS_TOKEN)}
        request = requests.get(DDA_ACCOUNTSDETAILS, headers=self.auth_headers)
        self.assertEqual(request.status_code, 200)

    def test_content_negotiation(self):
        pass