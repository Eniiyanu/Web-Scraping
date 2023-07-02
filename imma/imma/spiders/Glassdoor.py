import scrapy
from scrapy.loader import ItemLoader
from imma.items import Glassdoor
from urllib.parse import urlencode

import requests

API_KEY = '16ab3b0e-6c3e-40f8-b6b2-ef707e941f92'

def get_proxy_url(url):
    payload ={'api_key':API_KEY, 'url':url}
    proxy_url = 'https://proxy.scrapeops.io/v1/?' + urlencode(payload)
    return proxy_url


class GlassdoorSpider(scrapy.Spider):
    name = "Glassdoor"
    allowed_domains = ["glassdoor.com"]

    keywords = ["Contract", "Freelance", "Consultant"]

    def start_requests(self):
        start_url = 'https://www.glassdoor.com/Job/consultant-jobs-SRCH_KO0,10.htm?jobType=contract'
        proxy_url = get_proxy_url(start_url)
        yield scrapy.Request(url=proxy_url, callback=self.parse)

    def parse(self, response):
        jobs = response.css('a.d-flex.justify-content-between.p-std.jobCard')
        for job in jobs:
            job_url = job.attrib['href']
            if not job_url.startswith('http'):
                job_url = response.urljoin(job_url)
            proxy_url = get_proxy_url(job_url)
            yield response.follow(proxy_url, callback=self.parse_job_page)

    def parse_job_page(self, response):
        title = response.css('.css-1vg6q84.e1tk4kwz4::text').get()
        description =  response.css('.jobDescriptionContent.desc').get()
        if self.has_keywords(description):
            item = Glassdoor()
            item['job_title'] = response.css('.css-1vg6q84.e1tk4kwz4::text').get()
            item['company'] = response.css('.css-87uc0g.e1tk4kwz1::text').get()
            item['url'] = response.url
            item['location'] = response.css('.css-56kyx5.e1tk4kwz5').get()
            item['description'] = response.css('.jobDescriptionContent.desc').get()
            item['date_posted'] = response.css('.JobListing__Span-sc-15uyy2k-1.etpcIc::text').get()
            yield item

    def has_keywords(self, text):
        text = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
        return False
