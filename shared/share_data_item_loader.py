import csv
import pandas as pd
import argparse


class ShareDataItemLoader(object):
    def __init__(self, path_to_csv):
        self.path = path_to_csv

    def load_items(self, count):
        csv_file = pd.read_csv(self.path, nrows=count, delimiter=',')
        for index, row in csv_file.iterrows():
            # Create ShareDataItem record
            print(index)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Loads stocks historical data to database.')
    parser.add_argument('path', metavar='path', type=str, help='path to csv data')
    args = parser.parse_args()
    loader = ShareDataItemLoader(args.path)
    loader.load_items(52)
