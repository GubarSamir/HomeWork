import random
import string
import requests
from flask import Flask, request, Response
from webargs.flaskparser import use_kwargs
from webargs import fields, validate
import json

app = Flask(__name__)


def bitkoin(val='usd'):
    curs = str(val).upper()
    bit = requests.get(f'https://api.coindesk.com/v1/bpi/currentprice/{curs}.json')
    bit = bit.json()
    return f"{curs} to Bitkoin = {bit['bpi'][curs]['rate_float']}"


@app.route('/')
def hello_world():
    return 'Hello World'


@app.route('/random')
@use_kwargs({"length": fields.Int(required=True, validate=[validate.Range(min=1, max=999)]),
             "digits": fields.Boolean(required=False, missing=0, validate=[validate.Range(min=0, max=1)]),
             "specials": fields.Boolean(required=False, missing=0, validate=[validate.Range(min=0, max=1)])},
            location="query")
def get_random(length, digits, specials):
    random_base = string.ascii_lowercase
    if digits:
        random_base += string.digits
    if specials:
        random_base += string.punctuation
    result = ''.join(random.choices(random_base, k=length))
    return result


@app.route('/get_bitcoin_rate')
@use_kwargs({"currency": fields.String(required=True)}, location="query")
def get_bitcoin_rate(currency):
    return bitkoin(currency)


if __name__=='__main__':
    app.run()


app.run(debug=True, port=5000)
