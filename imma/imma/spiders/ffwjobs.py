import scrapy


class FfwjobsSpider(scrapy.Spider):
    name = "ffwjobs"
    allowed_domains = ["jobs.ffwd.org"]
    start_urls = ["https://jobs.ffwd.org/jobs"]

    def parse(self, response):
        jobs = response.css('a.sc-beqWaB.fZYMmZ.theme_only')
        for job in jobs:
            job_url = job.attrib['href']
            if not job_url.startswith('http'):
                job_url = response.urljoin(job_url)
            yield response.follow(job_url, callback=self.parse_job_page)

    def parse_job_page(self, response):
        title = response.css(
            '.PageLayout__Title-sc-1ri9r3s-4.fcPVcr::text').get()
        description = response.xpath(
            'normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2])').get()
        if self.has_keywords(description):
            yield {
                "url": response.url,
                "title": response.css('.PageLayout__Title-sc-1ri9r3s-4.fcPVcr::text').get(),
                "Location": response.xpath('normalize-space(//*[@id="jobPageBody"]/div[3]/div/div[2]/div[1])').get(),
                "Description": response.xpath('normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2])').get(),
                "Company": response.css('.CompanyCard__Title-gzvdxj-3.eaAofP::text').get(),
            }

            

    def has_keywords(self, text):
        text = text.lower()
        for keyword in self.keywords:
            if keyword.lower() in text:
                return True
        return False


"""

    yield {
                'Job': job.css('.ListCard__Title-sc-1dtq0w8-4::text').get(),
                'Company': job.css('div.ListCard__Title-sc-1dtq0w8-4.ListCard__Subtitle-sc-1dtq0w8-5::text').get(),
                'URL': 'https://climatebase.org/jobs'+job.css('a').attrib['href'],
                "Location":response.xpath('normalize-space(//*[@id="jobPageBody"]/div[3]/div/div[2]/div[1])').get()
                "Description":response.xpath('normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2]').get()
date posted :response.css('.JobListing__Span-sc-15uyy2k-1.etpcIc::text').get()   
            }

               """
