from urllib.parse import urlsplit, urlunsplit
from dotenv import load_dotenv
import os
import requests
import argparse


def shorten_link(token, url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    payload = {
        'long_url': url
    }
    response = requests.post(bitly_url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, url):
    url_parts = urlsplit(url)
    bitlink = f'{url_parts.netloc}{url_parts.path}'
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/' \
                f'{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(bitly_url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(token, url):
    url_parts = urlsplit(url)
    bitlink = f'{url_parts.netloc}{url_parts.path}'
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(bitly_url, headers=headers)
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    token = os.environ['BITLY_TOKEN']

    parser = argparse.ArgumentParser()
    parser.add_argument('link', help='ссылка')
    args = parser.parse_args()

    url = args.link
    if is_bitlink(token, url):
        try:
            clicks_count = count_clicks(token, url)
        except requests.exceptions.HTTPError:
            print('Ошибка при вводе битлинка')
        else:
            print('Количество переходов по битлинку:', clicks_count)
    else:
        try:
            bitlink = shorten_link(token, url)
        except requests.exceptions.HTTPError:
            print('Опечатка при вводе URL')
        else:
            print('Битлинк:', bitlink)
