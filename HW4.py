import os
import sqlite3
from flask import Flask, request, Response
from webargs.flaskparser import use_kwargs
from webargs import fields, validate
from flask import jsonify

app = Flask(__name__)

def execute_query(query, args=()):
    db_path = os.path.join(os.getcwd(), 'chinook.db')
    db_path = 'chinook.db'
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, args)
    conn.commit()
    records = cur.fetchall()
    return records

def format_records(lst):
    return '<br>'.join(str(elem) for elem in lst)

def clear_list(item):
    result = [j for i in item for j in i]
    return str(sum(result))


@app.route("/unique_names")
def get_unique_names():
    query = f"select FirstName from customers"
    records = execute_query(query)
    return str(len(set(records)))


@app.route("/tracks_count")
def get_tracks_count():
    query = f"SELECT COUNT(*) FROM tracks"
    records = execute_query(query)
    return clear_list(records)


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
        query += ' WHERE ' + ' AND '.join(f'{k}=\'{v}\'' for k, v in where_filter.items())
    records = execute_query(query)
    return format_records(records)


@app.route("/sales")
def get_sales():
    query = f"select SUM(UnitPrice * Quantity) from invoice_items"
    records = execute_query(query)
    return clear_list(records)


if __name__=='__main__':
    app.run()

app.run(debug=True, port=5000)
