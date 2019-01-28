import os
import hashlib
import sys
import xmltodict
import json

from datetime import datetime
from flask import Flask, session, render_template, request, flash
from flask_session import Session
from urllib.request import urlopen

app = Flask(__name__)

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    if not session.get('userid'):
        return render_template('login.html')
    else:
        return render_template("index.html")


@app.route("/convert/<string:amount>/<string:src_currency>/<string:dest_currency>/<string:reference_date>", methods=["GET"])
def convert(amount, src_currency, dest_currency, reference_date):

    data = {}
    if(amount is None):
        data['Error'] = "Amount is empty"
    elif(src_currency is None):
        data['Error'] = "Source currency is empty"
    elif(dest_currency is None):
        data['Error'] = "Destination currency is empty"
    else:
        rates = retrieve_rates()
        #print(rates)

        if(reference_date is None):
            max_date = rates.get('max_date')
        else:
            max_date = reference_date

        #print(max_date)

        if(dest_currency != "EUR"):
            rate_to_apply=rates[max_date][dest_currency];

            #print(rate_to_apply)

            if(src_currency == "EUR"):
                amount_new = float(amount)*float(rate_to_apply)
            else:
                rate_to_apply_src=rates[max_date][src_currency];
                amount_eur_src=float(amount)/float(rate_to_apply_src)
                #print(amount+" "+rate_to_apply_src+" "+str(amount_eur_src))
                amount_new = float(amount_eur_src)*float(rate_to_apply)
        else:
            if(src_currency == "EUR"):
                rate_to_apply = 1
                amount_new = float(amount)/float(rate_to_apply)
            else:
                rate_to_apply=rates[max_date][src_currency];
                amount_new = float(amount)/float(rate_to_apply)

        #print(amount_new)


        data['amount'] = amount_new
        data['currency'] = dest_currency
        json_data = json.dumps(data)
#    return amount_new
    return json_data


@app.route("/retrieve_rates")
def retrieve_rates():
    #with open('path/to/file.xml') as fd:
    xml=urlopen("https://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist-90d.xml").read()
#print(xml)
    doc = xmltodict.parse(xml)
    currencies = {}
    for xml_currencies_date in doc['gesmes:Envelope']['Cube']['Cube']:
        currencies_values = {}

        date_row = datetime.strptime(xml_currencies_date.get("@time"), '%Y-%M-%d')
        if(currencies.get('max_date') is None):
            currencies['max_date']='1970-01-01'

        max_date = datetime.strptime(currencies.get('max_date'), '%Y-%M-%d')
        if(date_row > max_date):
            currencies['max_date']=xml_currencies_date.get("@time")

        for xml_currencies_values in xml_currencies_date['Cube']:
            currencies_values[xml_currencies_values.get("@currency")]=xml_currencies_values.get("@rate")
            currencies[xml_currencies_date.get("@time")]=currencies_values

    #print(currencies)

    return currencies
