import json
import datetime
from typing import List

import fints_importer
import ynab

class FintsConfig:
    blz: str
    iban: str
    login: str
    pin: str
    fints_endpoint: str
    ynab_account_id: str
    parse_paypal: bool = False

    def __init__(self, bank_dict):
        # init fints bank config object from dict
        self.blz = bank_dict['blz']
        self.iban = bank_dict['iban']
        self.login = bank_dict['login']
        self.pin = bank_dict['pin']
        self.fints_endpoint = bank_dict['fints_endpoint']
        self.ynab_account_id = bank_dict['ynab_account_id']
        if 'parse_paypal' in bank_dict:
            self.parse_paypal = bank_dict['parse_paypal']

class Config:
    access_token: str
    budget_id: str
    cash_account_id: str = ''
    dry_run: bool = False
    fints: List[FintsConfig] = []

    def __init__(self, config_file_path: str):
        # init config pbjects with path to config file
        try:
            with open(config_file_path) as f:
                c_dict = json.load(f)
                self.access_token = c_dict['ynab']['access_token']
                self.budget_id = c_dict['ynab']['budget_id']
                if 'dry_run' in c_dict:
                    self.dry_run = c_dict['dry_run']
                if c_dict['ynab']['cash_account_id']:
                    self.cash_account_id = c_dict['ynab']['cash_account_id']

                self.fints = list(map(FintsConfig, c_dict['fints']))
                
        except FileNotFoundError:
            print("settings.json not found")
            exit()

if __name__ == "__main__":
    config = Config('settings.json')

    print(datetime.datetime.now().isoformat())

    for bank_config in config.fints:
        transactions = fints_importer.get_transactions(bank_config)

        if config.dry_run:
            print(transactions)
            print('Dry run, no transactions imported for this account')
            continue

        if transactions:
            print('')
            #ynab.send_transactions(config, bank_config, transactions)
        else:
            print('Account {bank_config.iban}: No transactions were found')
