from bs4 import BeautifulSoup
import requests
import flask
from flask import request, jsonify
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True

url = "https://databank.worldbank.org/reports.aspx?source=2&series=SL.UEM.TOTL.NE.ZS&country=#"

page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(page.content, 'html.parser')

# Year's
result = []
column = soup.find_all('table', id='grdTableView_DXHeaderTable')
for column_name in column:
    column_names = column_name.find_all('tr')

    for column_value in column_names:
        column_values = column_value.find_all('td')
        column_values = [x.text.strip() for x in column_values]
        if len(column_values[0]) != 0:
            for element in column_values:
                result.append(element)
while "" in result:
    result.remove("")
result.insert(0, 'Country')

# Data
Fresult = []
table = soup.find_all('table', id='grdTableView_DXMainTable')
for row in table:
    rows = row.find_all('tr')
    for row_val in rows:
        row_values = row_val.find_all('td')
        row_values = [x.text.strip() for x in row_values]
        res = dict(zip(result, row_values))
        # print(res)
        Fresult.append(res.copy())
print(Fresult)


# YEARS ###################


# years_HTML = soup.find_all(attrs={"name": "hdnAbobeText"})
# print(years_HTML)
# year = years_HTML[0]['value']
# year1 = (year.split('WDI_Time":',1)[1])
# year2 = (year1.split(',"WDI_Series')[0])
# print(year2)







# @app.route('/', methods=['GET'])
# def home():
#     return '''<h1>Distant Reading Archive</h1>
# <p>A prototype API for distant reading of science fiction novels.</p>'''
# @app.route('/api/v1/resources/unemployment', methods=['GET'])
# def api_all():
#     return jsonify(Fresult)
# @app.route('/api/v1/resources/year',methods=['GET'])
# def api_year():
#     return jsonify(year)
# app.run()
