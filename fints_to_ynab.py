import json
import datetime
import fints_importer
import ynab

def load_config():
    try:
        with open('settings.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("settings.json not found")
        exit()

config = load_config()

print(datetime.datetime.now().isoformat())

for bank_config in config['fints']:
    transactions = fints_importer.get_transactions(bank_config)

    if transactions:
        req = ynab.send_transactions(config['ynab'], bank_config['ynab_account_id'], transactions)
        if req:
            if 'error' in req:
                print(f'Account {bold(bank_config["iban"])}: YNAB import failed with Error: {req}')
            elif 'data' in req:
                if req['data']['duplicate_import_ids']:
                    print(f'Account {bank_config["iban"]}: {len(req["data"]["duplicate_import_ids"])} duplicate transations were not imported')
                    if req['data']['transaction_ids']:
                        print(f'Account {bank_config["iban"]}: {len(req["data"]["transaction_ids"])} transactions imported to YNAB')
        else:
            print('Connection to YNAB API failed')
    else:
        print('Account {bank_config["iban"]}: No transactions were found')
