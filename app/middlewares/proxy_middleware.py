import requests
from scrapy.core.downloader.handlers.http11 import TunnelError
from twisted.internet.error import ConnectionRefusedError, TimeoutError, TCPTimedOutError


class ProxyMiddleware(object):
    proxy_pool = []
    times = 9

    def process_request(self, request, spider):
        if len(self.proxy_pool) < 10:
            self._get_proxy()

        spider.logger.info(f"Number of valid: {len(self.proxy_pool)}")

        self.times = 0 if self.times >= 9 else self.times + 1
        spider.logger.info(f"GET {request.url} (Use Proxy: http://{self.proxy_pool[self.times]})")
        request.meta["proxy"] = "http://" + self.proxy_pool[self.times]

    def process_exception(self, request, exception, spider):
        if isinstance(exception, ConnectionRefusedError) or isinstance(exception, TimeoutError) \
                or isinstance(exception, TunnelError) or isinstance(exception, TCPTimedOutError):
            self.proxy_pool.pop(0)
            request.meta["proxy"] = "http://" + self.proxy_pool[self.times]
            return request

        raise exception

    def _get_proxy(self):
        res = requests.get("http://127.0.0.1:5010/get_all/")
        for proxy in res.json():
            self.proxy_pool.append(proxy)
