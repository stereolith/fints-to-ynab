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

transactions = fints_importer.get_transactions(config)

if transactions:
    req = ynab.send_transactions(config, transactions)
    if req:
        if 'error' in req:
            print(f'YNAB import failed with Error: {req}')
        elif 'data' in req:
            if req['data']['duplicate_import_ids']:
                print(f'{len(req["data"]["duplicate_import_ids"])} duplicate transations were not imported')
                if req['data']['transaction_ids']:
                    print(f'{len(req["data"]["transaction_ids"])} transactions imported to YNAB')
    else:
        print('Connection to YNAB API failed')
else:
    print('No transactions were found')
