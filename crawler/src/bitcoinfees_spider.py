import scrapy


class BitcoinFeesSpider(scrapy.Spider):
    name = 'bitcoinfees'
    start_urls = [
        'https://bitcoinfees.net/',
    ]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',

        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'en',
        }
    }

    def parse(self, response):
        fee_rates_table_body = response.css('tbody')
        for fee_rate_row in fee_rates_table_body.css('tr'):
            yield {
                'feeRate': fee_rate_row.css('tr').css('td:first-child::text').get(),
                'transactions': fee_rate_row.css('tr').css('td .progress .progress-bar::text').get(),
                'time': fee_rate_row.css('tr').css('td:last-child::text').get(),
            }
