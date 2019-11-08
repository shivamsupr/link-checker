import os
import urllib3
import json
import scrapy
from config.app_config import ApplicationConfig

class LinkCheckerSpider(scrapy.Spider):
    name = "link_checker_spider"
    custom_settings = {
        'HTTPERROR_ALLOW_ALL': True,
        'DEPTH_LIMIT': 50,
        'MAX_REQUESTS': 100000,
        'RETRY_HTTP_CODES': [],
    }

    def __init__(self, manifest_url, input_url, fetch_from_file='false', only_broken='false', *args, **kwargs):
        """Initializes the instance"""
        self.input_url = input_url
        self.only_broken = only_broken
        super(LinkCheckerSpider, self).__init__(*args, **kwargs)

        """Fetch manifest from specified URL"""
        http = urllib3.PoolManager()
        # urllib3.disable_warnings()
        request = http.request('GET', manifest_url)
        self.asset_json = json.loads(request.data)

        """Generate URL list to be crawl"""
        if fetch_from_file == 'true':
            """Fetch domain list"""
            with open(os.path.join(ApplicationConfig.get_shared_root(), self.filepath), 'r') as domains_file:
                domain_json = domains_file.read()

            domains = json.loads(domain_json)
            for domain in domains:
                for key, asset in self.asset_json['files'].items():
                    # print("{}{}".format(domain, asset))
                    self.start_urls.append("{}{}".format(domain, asset))
                # continue
        else:
            self.start_urls = [input_url]

    def start_requests(self):
        """Generates initial requests"""
        for url in self.start_urls:
            # Explicitly set the errback handler
            yield scrapy.Request(url, dont_filter=True, callback=self.parse, errback=self.errback)

    def parse(self, response):
        """Parses a default response"""
        if not isinstance(response, scrapy.http.TextResponse):
            self.crawler.stats.inc_value('non_text_response')
            return

        if self.only_broken == 'true':
            if response.status >= 400 and response.status <= 599:
                yield {
                    'url': response.url,
                    'status': 'invalid_http_status',
                    'http_status': response.status,
                }
        else:
            yield {
                'url': response.url,
                'http_status': response.status,
            }

        # max_reqs = self.settings.getint('MAX_REQUESTS', 0)
        # for key, asset in self.asset_json['files'].items():
        #     # self.start_urls.append("{}{}".format(domain, asset))
        #     yield scrapy.Request("{}{}".format(self.input_url, asset), callback=self.parse, errback=self.errback)

    def errback(self, err):
        """Handles an error"""
        return {
            'url': err.request.url,
            'status': 'error_downloading_http_response',
            'message': str(err.value),
        }
