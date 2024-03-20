# FinTS YNAB Importer

This Python script imports transactions from banks that support the German FinTS Banking API. 

The last 10 days of transactions are imported. It's safe to run this script periodically as duplicates (already imported transactions) are filtered out.

## Settings
Connection details need to be set up in a `settings.json` file in the project folder, see an example at `settings.sample.json`.

#### general options
- **dry_run**: (optional) If `true`, prevent sending transaction data to the YNAB API.

#### `"fints"` bank accounts
Multiple bank accounts can be setup in the array `"fints"`.
- **fints_endpoint**: This is the FinTS endpoint for your bank. An incomplete list of endpoints can be found [here](https://raw.githubusercontent.com/jhermsmeier/fints-institute-db/master/fints-institutes.json).
- **ynab_account_id**: Transactions fetched from this bank account are assigned to this YNAB account. In YNAB's web interface on the account page this is the last ID in the URL.
- **parse_paypal**: (optional): If `true`, the script tries to extract the merchant's name in PayPal transactions to avoid these transactions being assigned to the genreic *PayPal* payee. The memo of these transactions is set to *PayPal*.
- **tan_medium** (optional): Name of the tan medium to use ([fixes this issue with DKB bank](https://github.com/raphaelm/python-fints/issues/121))

#### `"ynab"`
- **access_token**: A YNAB API access token (Request it in the YNAB [developer settings](https://app.youneedabudget.com/settings/developer)).
- **budget_id**: In YNAB's web interface, this is the first ID in the URL.
- **cash_account_id** (optional): If set, transactions that are identified as cash withdrawls are imported as transfers to this account.

## Install
- requires at least python3.6 
- Install dependencies:
  `pip3 install -r requirements.txt`

## Run 
Run the script with:
`python3 fints_to_ynab.py`

### Crontab
This script can be run periodically with cron.
This example crontab entry runs the script every 3 hours and writes STDOUT to a logfile (adjust the path to the cloned repository and the python version):
`0 */3 * * * cd /path/to/fints-to-ynab/ && venv/bin/python3.6 fints_to_ynab.py >> import.log`
