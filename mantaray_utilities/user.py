"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""
import json
import logging
import csv
import os
import random
import time

from eth_account import Account as eth_account
from ocean_keeper.account import Account
from ocean_utils.http_requests.requests_session import get_requests_session
from ocean_utils.utils.utilities import get_timestamp
from urllib3 import request


def password_map(address, password_dict):
    """Simple utility to match lowercase addresses to the password dictionary

    :param address:
    :param password_dict:
    :return:
    """
    lower_case_pw_dict = {k.lower(): v for k, v in password_dict.items()}
    if str.lower(address) in lower_case_pw_dict:
        password = lower_case_pw_dict[str.lower(address)]
        return password
    else:
        return False


def load_passwords_environ():
    assert 'PASSWORD_PATH' in os.environ
    return load_passwords(os.environ['PASSWORD_PATH'])


def load_passwords(path_passwords):
    """Load password file into an address:password dictionary

    :param path_passwords:
    :return: dict
    """

    assert os.path.exists(path_passwords), "Password file not found: {}".format(path_passwords)
    passwords = dict()
    with open(path_passwords) as f:
        for row in csv.reader(f):
            if row:
                passwords[row[0]] = row[1]

    passwords = {k.lower(): v for k, v in passwords.items()}
    logging.info("{} account-password pairs loaded".format(len(passwords)))
    return passwords


def get_account(ocn):
    """Utility to get a random account
    Account exists in the environment variable for the passwords filej
    Account must have a password
    Account must have positive ETH balance

    :param ocn:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        # Only select accounts with positive ETH balance
        if ocn.accounts.balance(acct).eth/10**18 < 1:
            continue
        possible_accounts.append(acct)

    this_account = random.choice(possible_accounts)
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account


def get_account_by_index(ocn, acct_number):
    """Utility to get one of the available accounts by index (as listed in the password file)
    Account exists in the environment variable for the passwords file
    Account must have password

    :param ocn:
    :param acct_number:
    :return:
    """
    password_dict = load_passwords_environ()

    addresses = [str.lower(addr) for addr in password_dict.keys()]

    possible_accounts = list()
    for acct in ocn.accounts.list():
        # Only select the allowed accounts
        if str.lower(acct.address) not in addresses:
            continue
        possible_accounts.append(acct)

    this_account = possible_accounts[acct_number]
    this_account.password = password_map(this_account.address, password_dict)
    assert this_account.password, "No password loaded for {}".format(this_account.address)
    return this_account


def create_account(faucet_url=None, wait=True):
    timestamp = get_timestamp()
    private_key = eth_account.create(timestamp)
    account = Account(private_key.address, None, private_key=private_key.privateKey.hex())
    if faucet_url:
        request_ether(faucet_url, account, wait=wait)
    return account


def request_ether(faucet_url, account, wait=True):
    requests = get_requests_session()

    payload = {"address": account.address}
    response = requests.post(
        f'{faucet_url}/faucet',
        data=json.dumps(payload),
        headers={'content-type': 'application/json'}
    )
    try:
        response_json = json.loads(response.content)
        success = response_json.get('success', 'false') == 'true'
        if success and wait:
            time.sleep(5)

        return success, response_json.get('message', '')
    except Exception as err:
        print(f'Error parsing response {response}: {err}')
        return None, None
