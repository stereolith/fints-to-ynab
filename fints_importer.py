import re
from fints.client import FinTS3PinTanClient
from fints.utils import minimal_interactive_cli_bootstrap
from datetime import date, timedelta
from models import Transaction

def transform_paypal_transaction(payee, memo):
    if 'PayPal' in payee and 'Ihr Einkauf' in memo and 'AWV-MELDEPFLICHT' in memo:
        payee = memo[memo.find('Ihr Einkauf bei ') + 16 : memo.find('AWV-MELDEPFLICHT')]
        memo = 'PayPal'
    return payee, memo

def is_cash_withdrawl(transaction):
    if transaction['posting_text'] and "BARGELD" in transaction['posting_text']:
        return True
    return False

def transform_fints_transaction(transaction, parse_paypal=False):
    payee = ''
    if transaction['deviate_applicant']:
        payee = transaction['deviate_applicant']
    elif transaction['applicant_name']:
        payee = transaction['applicant_name']

    memo = transaction['purpose'] or ''

    if parse_paypal:
        payee, memo = transform_paypal_transaction(payee, memo)

    return Transaction(
        date=transaction['date'].isoformat(),
        amount=int(transaction['amount'].amount * 1000),
        payee=payee,
        memo=memo,
        cash_withdrawl = is_cash_withdrawl(transaction)
    )

def get_transactions(bank_config):
    f = FinTS3PinTanClient(
        bank_config.blz,
        bank_config.login,
        bank_config.pin,
        bank_config.fints_endpoint,
        product_id='33D93BB1B017D422A87837C01'
    )

    minimal_interactive_cli_bootstrap(f)

    with f:
        # Since PSD2, a TAN might be needed for dialog initialization. Let's check if there is one required
        if f.init_tan_response:
            print("A TAN is required", f.init_tan_response.challenge)
            tan = input('Please enter TAN:')
            f.send_tan(f.init_tan_response, tan)
        # Fetch accounts
        accounts = f.get_sepa_accounts()

    # get transactions
    account = next(filter(lambda a: a.iban == bank_config.iban, accounts), None)
    transactions = f.get_transactions(account, date.today()-timedelta(days=14))

    parsed_transactions = list(map(lambda t: transform_fints_transaction(t.data, parse_paypal=bank_config.parse_paypal), transactions))

    # filter paypal transactions (if configured)
    if bank_config.remove_paypal_transactions:
        parsed_transactions = list(filter(lambda t: not re.match('paypal', t.payee, re.IGNORECASE), parsed_transactions))

    return parsed_transactions
