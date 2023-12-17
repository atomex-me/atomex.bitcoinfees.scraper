import json
import requests
from datetime import timedelta

from flask import Flask

app = Flask(__name__)

MAX_FEE_VALUE = 1500


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
                idx = 0
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
                data = int((fee_from + fee_to) / 2)
            else:
                data = int(data)

            if 1 <= data <= MAX_FEE_VALUE:
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

    try:
        r = requests.get(url='https://bitcoinfees.earn.com/api/v1/fees/recommended')
        return r.json()
    except Exception as e:
        print(e)
        return {"fastestFee": MAX_FEE_VALUE, "halfHourFee": MAX_FEE_VALUE, "hourFee": MAX_FEE_VALUE}


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
