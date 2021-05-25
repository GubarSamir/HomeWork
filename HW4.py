import os
import sqlite3
from flask import Flask, request, Response
from webargs.flaskparser import use_kwargs
from webargs import fields, validate
from flask import jsonify

app = Flask(__name__)

def format_records(lst):
    return '<br>'.join(str(elem) for elem in lst)

def format_list(lst):
    return '<br>'.join(lst)


def execute_query(query, args=()):
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    db_path = 'chinook.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    records = cur.fetchall()
    return records


@app.route("/unique_names")
@use_kwargs({
    "first_name": fields.Str(
        required=False
    )},
    location="query"
)
def get_unique_names(first_name=None):
    query = f"select FirstName from customers"
    where_filter = {}
    if first_name:
        where_filter['FirstName'] = first_name
    if where_filter:
        query += ' WHERE ' + ' OR '.join(f'{k}=\'{v}\'' for k, v in where_filter.items())
    records = execute_query(query)
    return format_records(set(records))


@app.route("/tracks_count")
@use_kwargs({
    "get_name": fields.Str(
        required=False
    )},
    location="query"
)
def get_tracks_count(get_name=None):
    query = f"SELECT COUNT(*) FROM tracks"
    where_filter = {}
    if get_name:
        where_filter['Name'] = get_name
    if where_filter:
        query += ' WHERE ' + ' OR '.join(f'{k}=\'{v}\'' for k, v in where_filter.items())
    records = execute_query(query)
    return format_records(records)


@app.route("/")
@app.route("/customers")
@use_kwargs({
    "city": fields.Str(
        required=False
    ),
    "country": fields.String(
        required=False
    )},
    location="query"
)
def get_customers(city=None, country=None):
    query = f"select * from customers"
    where_filter = {}
    if city:
        where_filter['City'] = city
    if country:
        where_filter['Country'] = country
    if where_filter:
        query += ' WHERE ' + ' OR '.join(f'{k}=\'{v}\'' for k, v in where_filter.items())
    records = execute_query(query)
    return format_records(records)


@app.route("/sales")
def get_sales():
    unit_price = f"select UnitPrice from invoice_items"
    quantity = f"select Quantity from invoice_items"
    records = execute_query(quantity)
    records2 = execute_query(unit_price)

    return str(sum_price(records) * sum_price(records2))


def sum_price(item):
    summa = []
    for i in item:
        for j in i:
            summa.append(j)
    return sum(summa)



if __name__=='__main__':
    app.run()

app.run(debug=True, port=5000)
