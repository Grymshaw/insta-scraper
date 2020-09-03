import scrapy
import csv

from selenium import webdriver

TAGS = [
    'politics',
    'blacklivesmatter',
    'trump',
    'trump2020',
    'biden2020',
    # 'covid19',
]


class PostsSpider(scrapy.Spider):
    name = 'posts_spider'
    start_urls = [f'https://www.instagram.com/explore/tags/{t}' for t in TAGS]

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        tag = response.url.split('/')[-2]
        print('current tag: ', tag)

        outfile = 'posts.csv'
        with open(outfile, 'a+') as f:
            writer = csv.writer(f)
            # Only first 9 posts are "top posts"
            top_posts = self.driver\
                .find_elements_by_css_selector('.v1Nh3 a')[:9]

            for post in top_posts:
                c = post.get_attribute('href')
                writer.writerow([tag, c])

    def closed(self, reason):
        self.driver.quit()
