import argparse
import requests
import json
from datetime import date, timedelta


def get_news_api_payload(query, apikey, from_date, to_date):
    args = {
        'q'      : query,
        'sortBy' : 'popularity',
        'from'   : from_date,
        'to'     : to_date,
        'apiKey' : apikey
    }
    return args


def get_start_end_week_dates():
    today = date.today()
    week_before = today - timedelta(weeks=1)
    return week_before, today


def download_news_json(args):
    url = 'https://newsapi.org/v2/everything?'
    download = requests.get(url, params=args)
    print('Sending request for news ' + download.url)
    if download.status_code == requests.codes.ok:
        print("Successful request!")
        # decode binary content
        content_json = json.loads(download.content)
        articles = content_json['articles']
        return articles
    else:
        download.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads news from news API')
    parser.add_argument('query', metavar='query', type=str, help='search query')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private API key')
    parser.add_argument('print', metavar='print', type=bool, nargs='?', help='should print result')
    args = parser.parse_args()
    from_date, to_date = get_start_end_week_dates()
    articles = download_news_json(get_news_api_payload(args.query,
                                                       args.apikey,
                                                       from_date,
                                                       to_date))
    if args.print:
        for article in articles:
            print('\n', article['title'])
