from ynab_sdk import YNAB
from ynab_sdk.api.models.requests.transaction import TransactionRequest


def send_transactions(config, transactions):
    def create_request(transaction):
        return TransactionRequest(
            account_id=config['ynab']['account_id'],
            date=transaction.date,
            amount=transaction.amount,
            memo=transaction.memo,
            cleared=True,
            payee_name=transaction.payee
        )

    ynab = YNAB(config['ynab']['access_token'])

    transaction_req = list(map(create_request, transactions))

    ynab.transactions.create_transactions(config['ynab']['budget_id'], transaction_req)
