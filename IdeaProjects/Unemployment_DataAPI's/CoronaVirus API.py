from bs4 import BeautifulSoup
import requests
import flask
from flask import request, jsonify
import re

app = flask.Flask(__name__)
app.config["DEBUG"] = True

url = "https://www.worldometers.info/coronavirus/#countries"

page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(page.content, 'html.parser')

table = soup.find_all('table', id='main_table_countries_today')

header = ["Country", "TotalCases", "NewCases", "TotalDeaths", "NewDeaths", "TotalRecovered", "NewRocovered",
          "ActiveCases", "CriticalCases", "CasesIn1Mpop", "DeathsIn1Mpop", "TotalTests", "Tests1Mpop", "Population",
          "Continent", "1Case_Per_Xpeople", "1Death_Per_Xpeople", "1Test_Per_Xpeople"]

Fresult_world = []
Fresult_countries = []

for row in table:
    rows = row.find_all('tr')
    for row_val in rows:
        row_values = row_val.find_all('td')
        row_values = [x.text.strip() for x in row_values]
        if len(row_values) >= 12 and row_values[1] != "USA Total" and row_values[1] != "Total:" and len(
                row_values[0]) != 0:
            del row_values[0]
            res_world = dict(zip(header, row_values))
            Fresult_world.append(res_world.copy())
            Fresult_countries.append(row_values[0])


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


@app.route('/api/v1/coronavirus/world', methods=['GET'])
def api_worldData():
    return jsonify(Fresult_world)


@app.route('/api/v1/coronavirus/countrieslist', methods=['GET'])
def api_countries_list():
    return jsonify(Fresult_countries)

app.run()