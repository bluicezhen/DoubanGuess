import requests
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.error import ConnectionRefusedError


class ProxyMiddleware(object):
    proxy_pool = []

    def process_request(self, request, spider):
        if len(self.proxy_pool) == 0:
            self._get_proxy()
        request.meta["proxy"] = "http://" + self.proxy_pool[0]

    def process_exception(self, request, exception, spider):
        if isinstance(exception, ConnectionRefusedError):
            self.proxy_pool.pop(0)
            request.meta["proxy"] = "http://" + self.proxy_pool[0]
            return request

        if isinstance(exception, TunnelError):
            self.proxy_pool.pop(0)
            request.meta["proxy"] = "http://" + self.proxy_pool[0]
            return request

        raise exception

    def _get_proxy(self):
        res = requests.get("http://127.0.0.1:5010/get_all/")
        for proxy in res.json():
            self.proxy_pool.append(proxy)
