import argparse
from download_data import download_fx_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads historical data from alphavantage.')
    parser.add_argument('base_ccy', metavar='base_ccy', type=str, help='base currency (for e.g. EUR in EUR/USD)')
    parser.add_argument('ccy', metavar='ccy', type=str, help='instrument currency (for e.g. USD in EUR/USD)')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private api key')
    parser.add_argument('folder', metavar='folder', type=str, nargs='?', help='folder for storage')
    args = parser.parse_args()
    url = 'https://www.alphavantage.co/query?'
    download_fx_data(args.base_ccy, args.ccy, url, args.apikey, args.folder)