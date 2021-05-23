import statistics
import string
import flask
import pandas as pd
import faker
from statistics import mean
from flask import Flask

def Inches_to_cm(x):
    inch = x
    return inch * 2.54

def Pounds_to_kg(y):
    pou = y
    return pou * 0.45359237

ef = pd.read_csv('hw.csv')
He = [i for i in ef[' "Height(Inches)"']]
We = [i for i in ef[' "Weight(Pounds)"']]

Height = Inches_to_cm(statistics.mean(He))
Weight = Pounds_to_kg(statistics.mean(We))

with open("requirements.txt") as file:
    req = file.read()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/avr_data')
def get_avr_data():
    return f'Height={Height}, Weight={Weight}'


@app.route('/requirements')
def get_requirements():
    return str(req)

@app.route('/random_students')
def get_random_students():
    f = faker.Faker()
    std = [f.name()+',' for i in range(100)]
    return str(std)

if __name__ == '__main__':
    app.run()


app.run(debug=True)
