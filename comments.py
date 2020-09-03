import scrapy
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

post_urls = []
with open('posts.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        post_urls += [row[-1]]

print('post_urls:')
print(post_urls)


class InstaSpider(scrapy.Spider):
    name = 'insta_spider'
    # start_urls = ['https://www.instagram.com/p/CBHH2KjI6BW/']
    start_urls = post_urls

    def __init__(self):
        self.driver = webdriver.Firefox()

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)

        try:
            count = 0
            more_button = self.driver.find_element_by_css_selector(
                'button.dCJp8'
            )
            while (count < 10):
                more_button.click()
                count += 1
                more_button = WebDriverWait(self.driver, 3).until(
                    EC.presence_of_element_located(
                        By.CSS_SELECTOR,
                        'button.dCJp8'
                    )
                )
        except Exception:
            print('No more comments to fetch on this post!')

        outfile = 'comments.csv'
        with open(outfile, 'a+') as f:
            writer = csv.writer(f)
            comments = self.driver.find_elements_by_css_selector(
                'ul.Mr508 div.C4VMK span'
            )
            for comment in comments:
                c = comment.text
                writer.writerow([response.url, c])

    def closed(self, reason):
        self.driver.quit()
