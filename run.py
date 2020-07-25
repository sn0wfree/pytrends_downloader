# coding=utf-8
import os

from pytrends_downloader.server.server import api

if __name__ == '__main__':
    address = os.getenv('address', '0.0.0.0')
    PORT = os.getenv('PORT', 5672)
    api.run(address=address, port=PORT)
    pass
