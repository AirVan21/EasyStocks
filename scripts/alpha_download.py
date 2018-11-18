import argparse
import requests
import urllib.parse as url


def get_payload(symbol, apikey):
    args = {}
    args['function'] = 'TIME_SERIES_WEEKLY'
    args['datatype'] = 'csv'
    args['symbol'] = symbol
    args['apikey'] = apikey
    return args


def download_data(symbol, apikey='demo', folder=''):
    data_url = 'https://www.alphavantage.co/query?'
    download = requests.get(data_url, params=get_payload(symbol, apikey))
    print('Sending request for CSV to ' + download.url)
    content = download.content.decode('utf-8')
    with open(folder + '/' + symbol + '.csv', 'w') as output:
        output.write(content)


parser = argparse.ArgumentParser(description='Downloads historical data from alphavantage.')
parser.add_argument('symbol', metavar='symbol', type=str, help='stock symbol')
parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
args = parser.parse_args()


download_data(args.symbol, args.apikey, args.folder)
