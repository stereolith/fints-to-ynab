from ynab_sdk import YNAB
from ynab_sdk.api.models.requests.transaction import TransactionRequest


def send_transactions(ynab_config, ynab_account_id, transactions):
    ynab = YNAB(ynab_config['access_token'])

    transfer_payee_id = ""
    if ynab_config['cash_account_id'] != "":
        cash_account = ynab.accounts.get_account(ynab_config['budget_id'], ynab_config['cash_account_id'])
        transfer_payee_id = cash_account.data.account.transfer_payee_id

    def create_request(transaction):
        return TransactionRequest(
            account_id = ynab_account_id,
            date = transaction.date,
            amount = transaction.amount,
            memo = transaction.memo[:199] if transaction.memo else None,
            cleared = 'cleared',
            payee_name = transaction.payee if transfer_payee_id == "" else None,
            payee_id = transfer_payee_id if transfer_payee_id != "" else None,
            import_id = f'API:{transaction.amount}:{transaction.date}'
        )

    transaction_req = list(map(create_request, transactions))

    return ynab.transactions.create_transactions(ynab_config['budget_id'], transaction_req)
