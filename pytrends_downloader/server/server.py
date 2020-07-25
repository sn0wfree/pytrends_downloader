# coding=utf-8
import os

import responder

api = responder.API()

from pytrends_downloader.server.trends import GetTrends
from pytrends_downloader.proxy.get_proxy import get_proxy_with_default


@api.route("/google_trends/{greeting}")
async def greet_world(req, resp, *, greeting):
    if greeting == 'test':
        pass
    settings = req.params

    default_parameters = dict(cat=12, timeframe='all', geo='', gprop='')
    default_parameters.update(settings)

    resp.media = get_pytrends(**default_parameters)


def get_pytrends(kw_list: list, cat=12, timeframe='all', geo='', gprop=''):
    try:
        proxies = get_proxy_with_default(default='', raiseError=False)
        pytrends = GetTrends(hl='en-US', tz=360, timeout=(10, 25), proxies=proxies, retries=2,
                             backoff_factor=0.1, requests_args={'verify': False})
    except Exception as e:
        print(e)
        pytrends = GetTrends(hl='en-US', tz=360, timeout=(10, 25), proxies='', retries=2,
                             backoff_factor=0.1, requests_args={'verify': False})

    pytrends.set_tasks(kw_list, cat=cat, timeframe=timeframe, geo=geo, gprop=gprop)

    df = pytrends.interest_over_time().reset_index()
    df['date'] = df['date'].dt.strftime('%Y-%m-%d').tolist()
    # df = pd.DataFrame([[1, 2, 3], [2, 3, 4]], columns=['tes', '1'])
    print(df.head(1))
    result = df.to_dict('records')
    del pytrends
    return result
    # return {'test': "test"}


if __name__ == '__main__':
    address = os.getenv('address', '0.0.0.0')
    PORT = os.getenv('PORT', 5672)
    api.run(address=address, port=PORT)

# if __name__ == '__main__':
#     kw_list = ["Blockchain", "test"]
#     cat_list = """
#     Business & Industrial: 12
# Advertising & Marketing: 25
# Marketing Services: 83
# Loyalty Cards & Programs: 1309
# Public Relations: 327
# Search Engine Optimization & Marketing: 84
# Telemarketing: 328
# Aerospace & Defense: 356
# Defense Industry: 669
# Space Technology: 668
# Agriculture & Forestry: 46
# Agricultural Equipment: 748
# Aquaculture: 747
# Crops & Seed: 749
# Food Production: 621
# Forestry: 750
# Horticulture: 751
# Livestock: 752
# Automotive Industry: 1190
# Business Education: 799
# Business Finance: 1138
# Commercial Lending: 1160
# Investment Banking: 1139
# Risk Management: 620
# Venture Capital: 905
# Business News: 784
# Company News: 1179
# Company Earnings: 1240
# Mergers & Acquisitions: 1241
# Economy News: 1164
# Financial Markets: 1163
# Fiscal Policy News: 1165
# Business Operations: 1159
# Business Plans & Presentations: 336
# Human Resources: 157
# Compensation & Benefits: 723
# Corporate Training: 331
# Payroll Services: 724
# Recruitment & Staffing: 330
# Management: 338
# Business Process: 721
# Project Management: 1360
# Project Management Software: 1359
# Strategic Planning: 722
# Supply Chain Management: 801
# Business Services: 329
# Advertising & Marketing: 25
# Marketing Services: 83
# Loyalty Cards & Programs: 1309
# Public Relations: 327
# Search Engine Optimization & Marketing: 84
# Telemarketing: 328
# Consulting: 1162
# Corporate Events: 334
# Trade Shows & Conventions: 335
# E-Commerce Services: 340
# Merchant Services & Payment Systems: 280
# Fire & Security Services: 726
# Knowledge Management: 800
# Office Services: 28
# Office & Facilities Management: 337
# Office Supplies: 95
# Business Cards & Stationary: 1375
# Office Furniture: 333
# Printers, Copiers & Fax: 1330
# Copiers: 1331
# Fax Machines: 1332
# Ink & Toner: 1333
# Printers: 494
# Scanners: 495
# Outsourcing: 718
# Photo & Video Services: 576
# Stock Photography: 574
# Physical Asset Management: 719
# Quality Control & Tracking: 720
# Signage: 1076
# Writing & Editing Services: 725
#
#     """
#
#     proxies = ''  # ['https://34.203.233.13:80', 'https://35.201.123.31:880']
#     pytrends = TrendReq(hl='en-US', tz=360, timeout=(10, 25), proxies=proxies, retries=2,
#                         backoff_factor=0.1, requests_args={'verify': False})
#     pytrends.build_payload(kw_list, cat=12, timeframe='today 5-y', geo='', gprop='')
#
#     df = pytrends.interest_over_time()
#     df.to_csv('test.csv')
#     pytrends.build_payload(kw_list, cat=12, timeframe='all', geo='', gprop='')
#     df = pytrends.interest_over_time()
#     df.to_csv('test2.csv')
#     pass
