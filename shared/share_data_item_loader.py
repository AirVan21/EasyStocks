import argparse
import pandas as pd
import xml.etree.ElementTree as ET
from stocks.models import ShareDataItem, Share


class ShareDataItemLoader(object):
    '''
    ShareDataItemLoader class saves end-of-day data to the database
    '''

    def __init__(self, path_to_file):
        self.path = path_to_file

    def load_items_from_csv(self, share_ticker, count):
        '''
        Loads end-of-day data from the csv file to the database
        '''
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share for ticker', share_ticker)
            return
        csv_file = pd.read_csv(self.path, delimiter=',')
        csv_file['timestamp'] = pd.to_datetime(
            csv_file['timestamp'],
            errors='ignore'
        )
        csv_file.sort_values(by=['timestamp'], inplace=True, ascending=False)
        csv_file = csv_file.head(count)
        self.load_csv(share_items.first(), csv_file)

    def load_update(self, share_ticker):
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share!')
            return
        csv_file = pd.read_csv(self.path, delimiter=',')
        csv_file['timestamp'] = pd.to_datetime(
            csv_file['timestamp'],
            errors='ignore'
        )
        csv_file.sort_values(by=['timestamp'], inplace=True, ascending=False)
        # Last share data items
        selected_share = share_items.first()
        share_data_items = ShareDataItem.objects.filter(
            share=selected_share
        ).order_by('-date')
        if not share_data_items:
            self.load_csv(selected_share, csv_file)
        else:
            last_data_item = share_data_items.first()
            last_datetime = pd.to_datetime(last_data_item.date)
            csv_update = csv_file[csv_file['timestamp'] > last_datetime]
            self.load_csv(selected_share, csv_update)

    def load_csv(self, selected_share, csv_frame):
        '''
        Loads end-of-day data related to the share from the csv to database
        '''
        for index, row in csv_frame.iterrows():
            date_value = row['timestamp'].date()
            data_share_item = ShareDataItem(
                share=selected_share,
                date=date_value,
                open_price=row['open'],
                high_price=row['high'],
                low_price=row['low'],
                close_price=row['close'],
                volume=row['volume']
            )
            data_share_item.save()

    def load_moex_xml(self, date):
        '''
        Loads end-of-day data related to MOEX shares from the xml to database
        '''
        tree = ET.parse(self.path)
        root = tree.getroot()
        rows = root.findall('./data/rows/row')
        stocks_rus = Share.objects.filter(countryCode='RUS')
        ticker_to_stock_map = {}
        for stock in stocks_rus:
            ticker = stock.ticker
            if '.' in ticker:
                symbol, exchange = ticker.split('.')
                ticker_to_stock_map[symbol] = stock
        tqbr_rows = filter(lambda row: row.get('BOARDID') == 'TQBR', rows)
        for row in tqbr_rows:
            security_id = row.get('SECID')
            if security_id not in ticker_to_stock_map:
                continue
            else:
                open_value = row.get('OPEN')
                high_value = row.get('HIGH')
                low_value = row.get('LOW')
                close_value = row.get('CLOSE')
                volume_value = row.get('VOLUME')
                data_share_item = ShareDataItem(
                    share=ticker_to_stock_map[security_id],
                    date=date,
                    open_price=open_value,
                    high_price=high_value,
                    low_price=low_value,
                    close_price=close_value,
                    volume=volume_value
                )
                data_share_item.save()
                print(date, security_id, f'open = {open_value}, close = {close_value}')

    def clear_items(self, share_ticker):
        '''
        Removes share data items related to the share from the database
        '''
        share_items = Share.objects.filter(ticker=share_ticker)
        if not share_items:
            print('Did not find related share for ticker', share_ticker)
            return
        ShareDataItem.objects.filter(share=share_items.first()).delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads stocks historical data to database.')
    parser.add_argument('path', metavar='path', type=str, help='path to csv data')
    parser.add_argument('ticker', metavar='ticker', type=str, help='share ticker')
    args = parser.parse_args()
    # Loads
    loader = ShareDataItemLoader(args.path)
