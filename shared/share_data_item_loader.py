import pandas as pd
import argparse
from stocks.models import ShareDataItem, Share


class ShareDataItemLoader(object):
    def __init__(self, path_to_csv, share_ticker):
        self.path = path_to_csv
        self.ticker = share_ticker

    def load_items(self, count):
        share_items = Share.objects.filter(ticker=self.ticker)
        if not share_items:
            print('Did not find related share!')
            return
        csv_file = pd.read_csv(self.path, delimiter=',')
        csv_file['timestamp'] = pd.to_datetime(csv_file['timestamp'],
                                               errors='ignore')
        csv_file.sort_values(by=['timestamp'], inplace=True, ascending=False)
        csv_file = csv_file.head(count)
        for index, row in csv_file.iterrows():
            date_value = row['timestamp'].date()
            data_share_item = ShareDataItem(share=share_items.first(),
                                            date=date_value,
                                            open_price=row['open'],
                                            high_price=row['high'],
                                            low_price=row['low'],
                                            close_price=row['close'],
                                            volume=row['volume'])
            data_share_item.save()

    def clear_items(self):
        share_items = Share.objects.filter(ticker=self.ticker)
        if not share_items:
            print('Did not find related share!')
            return
        ShareDataItem.objects.filter(share=share_items.first()).delete()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads stocks historical data to database.')
    parser.add_argument('path', metavar='path', type=str, help='path to csv data')
    parser.add_argument('ticker', metavar='ticker', type=str, help='share ticker')
    args = parser.parse_args()
    # Loads
    loader = ShareDataItemLoader(args.path, args.ticker)
    loader.load_items(52)
