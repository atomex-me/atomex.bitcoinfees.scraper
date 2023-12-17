from scrapy.crawler import CrawlerProcess
from bitcoinfees_spider import BitcoinFeesSpider
from time import gmtime, strftime


def run():
    try:
        process = CrawlerProcess({
            'FEEDS': {
                'output/items.json': {
                    'format': 'json',
                    'overwrite': True,
                }
            }
        })
        process.crawl(BitcoinFeesSpider)
        process.start()
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print(f"Successfully crawled https://bitcoinfees.net at {time}")
    except Exception as ex:
        print(f"Error in crawler process {ex}")
        return


run()
