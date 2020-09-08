from dataclasses import dataclass

@dataclass()
class Transaction:
    date: str # ISO format (e.g. 2019-11-31)
    amount: int # amount in miliunits
    payee: str
    memo: str
    cash_withdrawl: bool
