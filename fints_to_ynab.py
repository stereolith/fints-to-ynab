import json
import fints_importer
import ynab
from tinydb import TinyDB, Query
import hashlib

def load_config():
    try:
        with open('settings.json') as f:
            return json.load(f)
    except FileNotFoundError:
        print("settings.json not found")
        exit()

def transaction_hash(transaction):
    return hashlib.md5(transaction.__repr__().encode()).hexdigest()

def filter_duplicates(transactions):
    Transaction = Query()
    return list(filter(lambda t: not db.search(Transaction.hash == transaction_hash(t)), transactions))


# database with hashed transactions for duplicate checking
db = TinyDB('db.json')

config = load_config()

transactions = fints_importer.get_transactions(config)
filtered_transactions = filter_duplicates(transactions)

for transaction in filtered_transactions:
    db.insert({'hash': transaction_hash(transaction)})


if filtered_transactions:
    ynab.send_transactions(config, filtered_transactions)
    print(f'{len(filtered_transactions)} transactions were imported to YNAB.')
else:
    print('No new transactions were imported to YNAB.')

