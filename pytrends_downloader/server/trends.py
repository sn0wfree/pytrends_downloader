# coding=utf-8
from pytrends_downloader.trends.request import TrendReq


class GetTrends(object):
    def __init__(self, hl='en-US', tz=360, timeout=(10, 25), proxies='', retries=2,
                 backoff_factor=0.1, requests_args={'verify': False}, kw_list=None):
        self.core = TrendReq(hl=hl, tz=tz, timeout=timeout, proxies=proxies, retries=retries,
                             backoff_factor=backoff_factor, requests_args=requests_args)
        self.kw_list = kw_list

    def set_tasks(self, kw_list, cat=12, timeframe='all', geo='', gprop='', ):
        self.kw_list = kw_list
        self.core.build_payload(kw_list, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)

    def interest_over_time(self):
        return self.core.interest_over_time()


if __name__ == '__main__':
    pass
