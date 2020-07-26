# coding=utf-8
import requests

HOST = '0.0.0.0'
url = f"http://{HOST}:5672/google_trends/test"

params = dict(kw_list=["Blockchain"], cat=12, timeframe='all', geo='', gprop='')
resp = requests.post(url, params=params)

if __name__ == '__main__':
    print(resp.content)
    pass
