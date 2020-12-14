import scrapy


class BitcoinFeesSpider(scrapy.Spider):
    name = 'bitcoinfees'
    start_urls = [
        'https://bitcoinfees.net/',
    ]

    def parse(self, response):
        fee_rates_table_body = response.css('tbody')
        for fee_rate_row in fee_rates_table_body.css('tr'):
            yield {
                'feeRate': fee_rate_row.css('tr').css('td:first-child::text').get(),
                'transactions': fee_rate_row.css('tr').css('td .progress .progress-bar::text').get(),
                'time': fee_rate_row.css('tr').css('td:last-child::text').get(),
            }
