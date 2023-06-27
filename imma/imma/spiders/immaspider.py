import scrapy
from imma.items import JobItem

class ImmaspiderSpider(scrapy.Spider):
    name = "immaspider"
    allowed_domains = ["climatebase.org"]
    start_urls = ["https://climatebase.org/jobs?"]
    keywords = ["Contract", "Freelance", "Consultant"]

    def parse(self, response):
        jobs = response.css('a.ListCard__ContainerLink-sc-1dtq0w8-0')
        for job in jobs:
            job_url = job.attrib['href']
            if not job_url.startswith('http'):
                job_url = response.urljoin(job_url)
            yield response.follow(job_url, callback=self.parse_job_page)

    def parse_job_page(self, response):
        title = response.css('.PageLayout__Title-sc-1ri9r3s-4.fcPVcr::text').get()
        description = response.xpath('normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2])').get()
        if self.has_keywords(description):
            item = JobItem()
            item['job_title'] = response.css('.PageLayout__Title-sc-1ri9r3s-4.fcPVcr::text').get()
            item['company'] = response.css('.CompanyCard__Title-gzvdxj-3.eaAofP::text').get()
            item['url'] = response.url
            item['location'] = response.xpath('normalize-space(//*[@id="jobPageBody"]/div[3]/div/div[2]/div[1])').get()
            item['description'] = response.xpath('normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2])').get()
            item['date_posted'] = response.css('.JobListing__Span-sc-15uyy2k-1.etpcIc::text').get()
            yield item

    def has_keywords(self, text):
        text = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
        return False

