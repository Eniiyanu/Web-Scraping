import scrapy


class Imma2Spider(scrapy.Spider):
    name = "imma2"
    allowed_domains = ["globalcharityjobs.com"]
    start_urls = ["https://globalcharityjobs.com/"]

    def parse(self, response):
        jobs = response.css(
            'a.et_pb_button et_pb_button_0 et_pb_bg_layout_light')
        for job in jobs:
            job_url = job.attrib['href']
            if not job_url.startswith('http'):
                job_url = response.urljoin(job_url)
            yield response.follow(job_url, callback=self.parse_job_page)

    def parse_job_page(self, response):
        title = response.css(
            '.et_pb_text_inner::text').get()
        description = response.css(
            '.et_pb_text_inner').get()
        # if self.has_keywords(description):
        yield {
            "url": response.url,
            "title": response.css('..et_pb_text_inner::text').get(),
            "Location": response.css('.et_pb_blurb_description').get(),
            "Description": response.xpath('normalize-space(//*[@id="jobPageBody"]/div[9]/ul[2])').get(),
            "Company": response.css('.CompanyCard__Title-gzvdxj-3.eaAofP::text').get(),
        }

    
