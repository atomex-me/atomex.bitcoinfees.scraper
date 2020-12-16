import json
import requests
from datetime import timedelta

from flask import Flask

app = Flask(__name__)


@app.route('/getbitcoinfees')
def main_route():
    try:
        with open('output/items_consistent.json') as json_file:
            json_file_string = json_file.read()
            json_file_string = remove_html_entities(json_file_string)
            data = json.loads(json_file_string)

            data = list(filter(lambda row: (time_from_str(row['time']) < timedelta(hours=1)), data))
            for row in data:
                row['transactions'] = int(row['transactions'])
            total_transactions_lower_hour = sum(row['transactions'] for row in data)

            if total_transactions_lower_hour > 1000:
                data.reverse()
                summ = 0
                idx = 1
                for row in data:
                    summ += row['transactions']
                    if summ > 1000:
                        break
                    idx += 1

                if idx == 0:
                    idx = 1
                data = data[idx - 1]['feeRate']
            else:
                data = data[1]['feeRate']

            if '-' in data:
                fee_from = int(data.split('-')[0])
                fee_to = int(data.split('-')[1])

                if fee_to - fee_from == 2:
                    data = fee_to - 1
                else:
                    data = fee_to
            else:
                data = int(data)

            if 10 <= data <= 400:
                data = {
                    'fastestFee': data,
                    'halfHourFee': data,
                    'hourFee': data,
                    'totalTxLowerOneHour': total_transactions_lower_hour
                }
            else:
                raise Exception('Fetched incorrect Fee!')
        return json.dumps(data)

    except Exception as e:
        print(e)
        r = requests.get(url='https://bitcoinfees.earn.com/api/v1/fees/recommended')
        return r.json()


def remove_html_entities(json_string):
    return json_string \
        .replace('221e', '1Y') \
        .replace('00a0', '') \
        .replace('\\u', '')


def time_from_str(time_string):
    if time_string[-1] == 'M':
        return timedelta(minutes=int(time_string[:-1]))
    if time_string[-1] == 'H':
        return timedelta(hours=int(time_string[:-1]))
    if time_string[-1] == 'D':
        return timedelta(days=int(time_string[:-1]))
    if time_string[-1] == 'Y':
        return timedelta(days=(365 * int(time_string[:-1])))
