# coding=utf-8
import json

import pandas as pd
import requests

HOST = '154.209.64.104'
PORT = 5672
url = f"http://{HOST}:{PORT}/google_trends/test"


def get_trends(kw_list, cat=12, timeframe='all', geo='', gprop=''):
    params = dict(kw_list=kw_list, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)
    resp = requests.post(url, params=params)
    status_code = resp.status_code
    # print(status_code)
    if status_code == 200:
        df = pd.DataFrame(json.loads(resp.content))
        return df
    else:
        return None


if __name__ == '__main__':
    df = get_trends(kw_list=['tisd',])
    print(df)
    pass
