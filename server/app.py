from flask import Flask
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    with open('output/items_consistent.json') as json_file:
        data = json.load(json_file)
        return json.dumps(data)
    return ''
