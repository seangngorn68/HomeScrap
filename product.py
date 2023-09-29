import json

import scrapy

class GoldOneComputerSpider(scrapy.Spider):
    name = "product"
    def start_requests(self):
        yield scrapy.Request(url="https://www.goldonecomputer.com/", callback=self.parse)

    def parse(self, response):
        category_links = response.xpath("//*[@class='box-content']/ul[@id='nav-one']/li/a/@href").getall()
        for category_link in category_links:
            ob_category_link = response.urljoin(category_link)
            yield response.follow(ob_category_link, callback=self.parse_category)
    def parse_category(self, response):
        # print(product_links, "This product link")
        print("This response:",response)
        product_links = response.xpath("//*[@class='caption']/h4/a/@href").getall()
        # Yield the product links.
        for product_link in product_links:
            ob_product_link = response.urljoin(product_link)
            yield response.follow(ob_product_link, callback=self.parse_product)
    def parse_product(self, response):
        product_information = {}
        product_information["code"] = response.xpath('//*[@id="content"]/div[1]/div[2]/ul[1]/li[2]/text()').get(),
        product_information["title"] = response.xpath('//*[@id="content"]/div[1]/div[2]/h3/text()').get(),
        product_information["brand"] = response.xpath("//ul[@class='list-unstyled']/li/a/text()").get(),
        product_information["price"] = response.xpath("//ul[@class='list-unstyled price']/li/h3/text()").get(),
        product_information["review_count"] = response.xpath(
                                   "//div[@class='rating-wrapper']/a[@class='review-count']/text()").get(),
        product_information["image"] = response.xpath('//*[@id="tmzoom"]/@src').get()
        with open("product_information.json", "a") as f:
            json.dump(product_information, f, indent=4)
        yield product_information