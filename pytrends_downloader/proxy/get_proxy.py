# coding=utf-8
import os
import re

import requests

from pytrends_downloader.utils.retry_it import conn_try_again

proxy_host = os.getenv('PROXY_HOST', '154.209.64.104')
proxy_port = int(os.getenv('PROXY_PORT', 5010))


class ArgumentError(Exception):
    """Raised when an invalid or conflicting function argument is supplied.

    This error generally corresponds to construction time state errors.

    """


class NoProxyError(Exception):
    pass


@conn_try_again(max_retries=2, default_retry_delay=2, expect_error=NoProxyError)
def get_proxy():
    proxy = requests.get(f"http://{proxy_host}:{proxy_port}/get/").content
    print(proxy)
    if proxy == b'no proxy!':
        raise NoProxyError('no proxy!')
    else:
        return parse_host_port(proxy)


def get_proxy_with_default(default='', raiseError=False, try_proxy='217.61.127.14:80'):
    try:
        proxy = get_proxy()
        proxy = check_proxy(proxy)
        if isinstance(try_proxy, str):
            try_proxy = check_proxy(parse_host_port(try_proxy))

        if isinstance(try_proxy, list):
            if isinstance(proxy, str) and proxy == '':
                proxy = try_proxy
            elif isinstance(proxy, list):
                proxy.extend(try_proxy)
            else:
                pass
        return proxy
    except Exception as e:
        if raiseError:
            raise e
        else:
            return default


def check_proxy(proxy_dict):
    if isinstance(proxy_dict, dict):
        proxies = {
            "http": f"http://{proxy_dict['host']}:{proxy_dict['port']}",
        }
        try:
            resp = requests.get("http://www.google.com", proxies=proxies, timeout=(20, 25))
            if resp.status_code != 200:
                print(resp.status_code)
                return ''
            else:
                return [f"{proxy_dict['host']}:{proxy_dict['port']}"]
        except Exception as e:
            print(e)
            return ''
    elif isinstance(proxy_dict, list):
        h = []
        for p in proxy_dict:
            res = check_proxy(p)
            if res == '':
                pass
            else:
                h.extend(res)
        if len(h) == 0:
            return ''
        else:
            return h
    else:
        return ''


def parse_host_port(text):
    if isinstance(text, bytes):
        text = text.decode()
    pattern = re.compile(r'''(?:
                (?:
                    \[(?P<ipv6host>[^/]+)\] |
                    (?P<ipv4host>[^/:]+)
                )?
                (?::(?P<port>[^/]*))?
            )?''', re.X)
    m = pattern.match(text)

    if m is not None:
        components = m.groupdict()
        ipv4host = components.pop('ipv4host')
        ipv6host = components.pop('ipv6host')

        components['host'] = ipv4host or ipv6host
        components['port'] = int(components['port'])
    else:
        raise ArgumentError(
            "Could not parse rfc1738 URL from string '%s'" % text)

    return components


def delete_proxy(proxy):
    requests.get(f"http://{proxy_host}:{proxy_port}/delete/?proxy={proxy}")


if __name__ == '__main__':
    c = get_proxy_with_default()
    # ccd = check_proxy(parse_host_port(b'58.250.21.56:3128'))
    print('return:', c, type(c))

    pass
