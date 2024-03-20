import pytest
from mt940.models import Date, Amount

from fints_importer import transform_fints_transaction
from fints_to_ynab import FintsConfig, Config

# fixtures & helper functions

def mock_fints_transaction(purpose, applicant_name, posting_text):
    amount = -50.00
    date_day = 10
    date_month = 11
    date_year = 2019
    return {
        'status': 'D',
        'funds_code': 'R',
        'amount': Amount(str(amount), 'D', 'EUR'),
        'id': 'N010',
        'extra_details': '',
        'currency': 'EUR',
        'date': Date(year=date_year, month=date_month, day=date_day),
        'entry_date': Date(year=date_year, month=date_month, day=date_day),
        'guessed_entry_date': Date(year=date_year, month=date_month, day=date_day),
        'transaction_code': '100',
        'posting_text': posting_text,
        'prima_nota': '0000',
        'purpose': purpose,
        'applicant_bin': 'ABCDEFMMXXX',
        'applicant_iban': 'DE12345678912345678901',
        'applicant_name': '',
        'return_debit_notes': '011',
        'deviate_applicant': applicant_name
    }

date = Date(year=2019, month=11, day=10)

@pytest.fixture
def mock_settings_file_path():
    return 'settings.sample.json'

@pytest.fixture
def mock_fints_transaction_regular():
    return mock_fints_transaction('2020-01-01T10.00Debitk.1 2020-01', 'REWE Regiemarkt GmbH', 'DIG. KARTE (APPLE PAY)')

@pytest.fixture
def mock_fints_transaction_cash():
    return mock_fints_transaction('2020-01-01T10.00Debitk.1 2020-01', 'SPARKASSE STADT', 'BARGELDAUSZAHLUNG')

@pytest.fixture
def mock_fints_transaction_paypal():
    return mock_fints_transaction('. APPLE STORE, Ihr Einkauf bei APPLE STOREAWV-MELDEPFLICHT BEACHTENHOTLINE BUNDESBANK.(0800) 1234-111', 'PayPal Europe S.a.r.l. et Cie S.C.A', 'FOLGELASTSCHRIFT')


# tests

def test_config(mock_settings_file_path):
    config = Config(mock_settings_file_path)

    assert config.access_token == 'xxx'
    assert config.budget_id == '123'
    assert config.cash_account_id == ''
    print(config.fints)
    assert len(config.fints) == 1

    bank = config.fints[0]
    assert bank.blz == "12345678"
    assert bank.iban == "DE1234567891234567890"
    assert bank.login == "user"
    assert bank.pin == "01234"
    assert bank.tan_medium == "iPhoneTan"
    assert bank.fints_endpoint == "https://banking-dkb.s-fints-pt-dkb.de/fints30"
    assert bank.ynab_account_id == "123"
    assert bank.parse_paypal == True


def test_regular_transaction_transformer(mock_fints_transaction_regular):
    transformed_transaction = transform_fints_transaction(mock_fints_transaction_regular)

    assert transformed_transaction.date == date.isoformat()
    assert transformed_transaction.memo == '2020-01-01T10.00Debitk.1 2020-01'
    assert transformed_transaction.payee == 'REWE Regiemarkt GmbH'
    assert transformed_transaction.cash_withdrawl == False


def test_cash_transaction_transformer(mock_fints_transaction_cash):
    transformed_transaction = transform_fints_transaction(mock_fints_transaction_cash)

    assert transformed_transaction.date == date.isoformat()
    assert transformed_transaction.memo == '2020-01-01T10.00Debitk.1 2020-01'
    assert transformed_transaction.payee == 'SPARKASSE STADT'
    assert transformed_transaction.cash_withdrawl == True


def test_paypal_transaction_transformer(mock_fints_transaction_paypal):
    transformed_transaction = transform_fints_transaction(mock_fints_transaction_paypal, parse_paypal=True)

    assert transformed_transaction.date == date.isoformat()
    assert transformed_transaction.memo == 'PayPal'
    assert transformed_transaction.payee == 'APPLE STORE'
    assert transformed_transaction.cash_withdrawl == False
