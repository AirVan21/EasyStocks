import requests


def get_share_payload(symbol, apikey):
    args = {
        'function': 'TIME_SERIES_WEEKLY',  # Period
        'datatype': 'csv',                 # Format
        'symbol': symbol,                  # Stock symbol
        'apikey': apikey                   # Private user identifier
    }
    return args


def get_fx_payload(base_ccy, ccy, apikey):
    args = {
        'function': 'FX_DAILY',
        'datatype': 'csv',
        'from_symbol': base_ccy,
        'to_symbol': ccy,
        'apikey': apikey
    }
    return args


def get_world_trading_data_payload(symbol, apikey):
    args = {
        'symbol': symbol,
        'api_token': apikey,
        'sort': 'newest',
        'output': 'csv',
    }
    return args


def download_data_csv(symbol, data_url, request_args, apikey, folder):
    download = requests.get(data_url, params=request_args)
    print('Sending request for CSV to ' + download.url)
    if download.status_code == requests.codes.ok:
        print("Successful request!")
    else:
        download.raise_for_status()
    # decode binary content
    content = download.content.decode('utf-8')
    # store content to data folder
    output_name = folder + '/' + symbol + '.csv'
    with open(output_name, 'w') as output:
        output.write(content)
        print('CSV is saved into: ' + output_name)


def download_share_data_alpha(symbol, url, apikey='demo', folder=''):
    payload = get_share_payload(symbol, apikey)
    download_data_csv(symbol, url, payload, apikey, folder)


def download_share_data_wtd(symbol, url, apikey='demo', folder=''):
    payload = get_world_trading_data_payload(symbol, apikey)
    download_data_csv(symbol, url, payload, apikey, folder)


def download_fx_data(base_ccy, ccy, url, apikey='demo', folder=''):
    payload = get_fx_payload(base_ccy, ccy, apikey)
    symbol = base_ccy + ccy
    download_data_csv(symbol, url, payload, apikey, folder)
