import requests
from datetime import datetime
from shared.data_reader_moex import DataReaderMOEX


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


def get_marketstack_payload(symbol, apikey):
    '''
    Returns URL arguments for the request to Marketstack
    '''
    args = {
        'access_key': apikey,
        'symbols': symbol,
        'limit': 500
    }
    return args


def get_moex_payload(date, start=0):
    '''
    Returns URL arguments for the request to MOEX
    '''
    args = {
        'limit': 100,
        'date': date.strftime('%Y-%m-%d'),
        'start': start
    }
    return args


def download_data_csv(symbol, data_url, request_args, folder):
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
    return output_name


def download_data_json(symbol, data_url, request_args, folder):
    download = requests.get(data_url, params=request_args)
    print('Sending request for JSON to ' + download.url)
    if download.status_code == requests.codes.ok:
        print("Successful request!")
    else:
        download.raise_for_status()
    # decode binary content
    content = download.content.decode('utf-8')
    # store content to data folder
    output_name = folder + '/' + symbol + '.json'
    with open(output_name, 'w') as output:
        output.write(content)
        print('JSON is saved into: ' + output_name)
    return output_name


def download_data_xml(date, data_url, request_args, folder):
    download = requests.get(data_url, params=request_args)
    print('Sending request for XML to ' + download.url)
    if download.status_code == requests.codes.ok:
        print("Successful request!")
    else:
        download.raise_for_status()
    # decode binary content
    content = download.content.decode('utf-8')
    # store content to data folder
    output_name = folder + '/moex-' + date.strftime('%Y-%m-%d') + '-' \
        + str(request_args['start']) + '.xml'
    with open(output_name, 'w') as output:
        output.write(content)
        print('XML is saved into: ' + output_name)
    return output_name


def download_share_data_alpha(symbol, url, apikey='demo', folder=''):
    payload = get_share_payload(symbol, apikey)
    return download_data_csv(symbol, url, payload, folder)


def download_share_data_wtd(symbol, url, apikey='demo', folder=''):
    payload = get_world_trading_data_payload(symbol, apikey)
    return download_data_csv(symbol, url, payload, folder)


def download_share_data_marketstack(symbol, url, apikey='demo', folder=''):
    payload = get_marketstack_payload(symbol, apikey)
    return download_data_json(symbol, url, payload, folder)


def download_share_data_moex(date, url, start=0, folder=''):
    payload = get_moex_payload(date, start)
    return download_data_xml(date, url, payload, folder)


def download_share_data_moex_full(date, url, folder=''):
    start = 0
    date = datetime.strptime(date, '%Y-%m-%d')
    payload = get_moex_payload(date, start)
    first_page = download_share_data_moex(date, url, start, folder)
    dataReader = DataReaderMOEX(first_page)
    total_rows = dataReader.get_total_rows()
    limit_value = payload['limit']
    page_names = [first_page]
    for start_value in range(limit_value, total_rows, limit_value):
        page_name = download_share_data_moex(date, url, start_value, folder)
        page_names.append(page_name)
    return page_names


def download_fx_data(base_ccy, ccy, url, apikey='demo', folder=''):
    payload = get_fx_payload(base_ccy, ccy, apikey)
    symbol = base_ccy + ccy
    download_data_csv(symbol, url, payload, folder)
