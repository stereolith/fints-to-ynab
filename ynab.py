from ynab_sdk import YNAB
from ynab_sdk.api.models.requests.transaction import TransactionRequest


def send_transactions(config, transactions):
    ynab = YNAB(config['ynab']['access_token'])

    transfer_payee_id = ""
    if config['ynab']['cash_account_id'] != "":
        cash_account = ynab.accounts.get_account(config['ynab']['budget_id'], config['ynab']['cash_account_id'])
        transfer_payee_id = cash_account.data.account.transfer_payee_id

    def create_request(transaction):
        return TransactionRequest(
            account_id = config['ynab']['account_id'],
            date = transaction.date,
            amount = transaction.amount,
            memo = transaction.memo[:199] if transaction.memo else None,
            cleared = 'cleared',
            payee_name = transaction.payee if transfer_payee_id == "" else None,
            payee_id = transfer_payee_id if transfer_payee_id != "" else None,
            import_id = f'API:{transaction.amount}:{transaction.date}'
        )

    transaction_req = list(map(create_request, transactions))

    return ynab.transactions.create_transactions(config['ynab']['budget_id'], transaction_req)
