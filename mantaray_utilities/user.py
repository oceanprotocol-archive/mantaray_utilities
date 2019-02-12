"""
The User() class, a helper class for simulating users of Ocean Protocol.
"""
import logging
import configparser
import logging
from .config import get_config_file_path, get_deployment_type, get_project_path
from squid_py.ocean.ocean import Ocean
from pathlib import Path
# assert PATH_CONFIG.exists(), "{} does not exist".format(PATH_CONFIG)
PATH_CONFIG = get_config_file_path()
import csv
import os

def password_map(acct, password_dict):
    return "asdf"

def load_passwords(path_passwords):
    # %%
    # Get all passwords
    assert os.path.exists(path_passwords)
    passwords = dict()
    # path_passwords = get_project_path() / 'passwords.csv'
    with open(path_passwords) as f:
        for row in csv.reader(f):
            if row:
                passwords[row[0]] = row[1]

    passwords = {k.lower(): v for k, v in passwords.items()}
    return passwords
