import urllib3


def get_http_result(url=None, method='GET', headers=None):
    http = urllib3.PoolManager()
    r = http.request(method, url)
    if 200 == r.status:
        return r.data.decode('utf-8')
    else:
        return None
