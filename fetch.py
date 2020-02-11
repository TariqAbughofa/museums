import requests
from html.parser import HTMLParser
import pandas as pd
import os

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_table = False
        self.in_row = False
        self.in_cell = False
        self.has_data = False
        self.data = []
        self.row = []

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            self.in_table = True
        elif tag == 'tr':
            self.in_row = True
        elif tag == 'td':
            self.in_cell = True
            self.has_data = False

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        elif tag == 'tr':
            self.in_row = False
            if self.row:
                self.data.append(self.row)
                self.row = []
        elif tag == 'td':
            self.in_cell = False

    def handle_data(self, data):
        if self.in_table and self.in_row and self.in_cell and not self.has_data:
            data = data.strip().replace(',', '')
            if data:
                self.has_data = True
                self.row.append(data)

URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {'format': 'json', 'action': 'parse', 'page': 'List of most visited museums'}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
html = data['parse']['text']['*']

parser = MyHTMLParser()
parser.feed(html)

df = pd.DataFrame(parser.data, columns=["name", "city", "vistors per year", "year reporteds"])

df['vistors per year'] = df['vistors per year'].apply(lambda x: int(x.replace(',', '')))

current_path = os.path.dirname(os.path.realpath(__file__))
df.to_csv(current_path+'/museums.csv', header=False, index=False)
