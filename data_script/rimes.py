#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import sys

RIMES_URL = "https://www.rimessolides.com/rime.aspx?t=R"

mot = sys.argv[1]

r = requests.get(RIMES_URL, params={
    'm': mot.lower()
})
soup = BeautifulSoup(r.text, 'lxml')

rimes = (a.text for a in soup.select('#divResultat > div > div.col-motrime > a'))

for rime in rimes:
    print(rime)
