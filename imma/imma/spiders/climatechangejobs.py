import scrapy
from scrapy.loader import ItemLoader
from imma.items import Unicef

class ClimatechangejobsSpider(scrapy.Spider):
    name = "climatechangejobs"
    allowed_domains = ["unicef.org"]
    start_urls = ["https://jobs.unicef.org/en-us/listing/?pagenotfound=true"]
    keywords = ["Contract", "Freelance", "Consultant"]

    def parse(self, response):
        jobs = response.css('a.job-link')
        for job in jobs:
            job_url = job.attrib['href']
            if not job_url.startswith('http'):
                job_url = response.urljoin(job_url)
            yield response.follow(job_url, callback=self.parse_job_page)

        next_page_url = response.css('a.more-link.button::attr(href)').get()
        if next_page_url:
            if not next_page_url.startswith('http'):
                next_page_url = response.urljoin(next_page_url)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_job_page(self, response):
        title = response.xpath('normalize-space(//*[@id="job-content"]/h2)').get()
        location = response.xpath('normalize-space(//*[@id="job-content"]/p[1]/span[4])').get()
        company = response.xpath('normalize-space(//*[@id="job-content"]/p[3]/a[2])').get()
        description = response.css('#job-details').get()

        if self.has_keywords(title):
            loader = ItemLoader(item=Unicef(), response=response)
            loader.add_value('url', response.url)
            loader.add_value('title', title)
            loader.add_value('location', location)
            loader.add_value('company', company)
            loader.add_value('description', description)
            yield loader.load_item()

    def has_keywords(self, text):
        text = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
        return False
