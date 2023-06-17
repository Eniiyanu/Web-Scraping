import scrapy


class ImmaspiderSpider(scrapy.Spider):
    name = "immaspider"
    allowed_domains = ["climatebase.org"]
    start_urls = ["https://climatebase.org/jobs?"]

    def parse(self, response):
        jobs = response.css('a.ListCard__ContainerLink-sc-1dtq0w8-0')

        for job in jobs:
            yield{
                'Job':job.css('.ListCard__Title-sc-1dtq0w8-4::text').get(),
                'URL':job.css('a').attrib['href'],
                'Location':job.css('.ListCard__Metadata-sc-1dtq0w8-7 .MetadataInfo__MetadataInfoStyle-hif7kv-1 ::text').get(),

            }
