import argparse
import requests
import json


def get_news_api_payload(query, apikey):
    args = {
        'q'      : query,
        'sortBy' : 'popularity',
        'apiKey' : apikey
    }
    return args


def download_news_json(url, args):
    download = requests.get(url, params=args)
    print('Sending request for news ' + download.url)
    if download.status_code == requests.codes.ok:
        print("Successful request!")
        # decode binary content
        content_json = json.loads(download.content)
        articles = content_json['articles']
        for article in articles:
            print(article)
    else:
        download.raise_for_status()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Downloads news from news API.')
    parser.add_argument('query', metavar='query', type=str, help='search query')
    parser.add_argument('apikey', metavar='apikey', type=str, help='private API key')
    args = parser.parse_args()
    url = 'https://newsapi.org/v2/everything?'
    download_news_json(url, get_news_api_payload(args.query, args.apikey))