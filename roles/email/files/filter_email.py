#! /usr/bin/python3

from bs4 import BeautifulSoup
import fileinput
import sys
import argparse
import re

#parser = argparse.ArgumentParser(description='Prefilter HTML')
#parser.add_argument('htmlfile', required=False)
#args = parser.parse_args()
html = ""
for line in fileinput.input():
    html += line

html.replace('<o:p>', '')
html.replace('<\o:p>', '')
html = re.sub('mso-bookmark:_[A-Za-z0-9]*', '', html)

soup = BeautifulSoup(html, features="lxml")

for match in soup.find_all(text=re.compile('^\xa0$')):
    match.parent.unwrap()

for match in soup.find_all('span', attrs={"style": "mso-fareast-language:EN-US"}):
    match.unwrap()

for match in soup.find_all('span', attrs={"style": "mso-fareast-language:EN-GB"}):
    match.unwrap()

for match in soup.find_all('span', attrs={"style": ""}):
    match.unwrap()

#<div class="WordSection1">
for match in soup.find_all('div', attrs={"class": "WordSection1"}):
    match.unwrap()

for match in soup.find_all('a'):
    href = True
    try:
        href = match['href']
    except KeyError:
        href = False

    if not href:
        match.unwrap()

print soup()

