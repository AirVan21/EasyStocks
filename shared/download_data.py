import requests


def get_payload(symbol, apikey):
    args = {
        'function' : 'TIME_SERIES_WEEKLY', # Period
        'datatype' : 'csv',                # Format
        'symbol'   : symbol,               # Stock symbol
        'apikey'   : apikey                # Private user identifier
    }
    return args


def download_data(symbol, apikey='demo', folder=''):
    data_url = 'https://www.alphavantage.co/query?'
    download = requests.get(data_url, params=get_payload(symbol, apikey))
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
