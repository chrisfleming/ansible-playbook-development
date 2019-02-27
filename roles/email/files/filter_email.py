#! /usr/bin/python3

from bs4 import BeautifulSoup
import fileinput
import sys
import argparse
import re
import io

#parser = argparse.ArgumentParser(description='Prefilter HTML')
#parser.add_argument('htmlfile', required=False)
#args = parser.parse_args()
html = ""

encoding = 'utf-8'
encoding = sys.argv[1]

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding=encoding)
for line in input_stream:
    html += line

html.replace('<o:p>', '')
html.replace('<\o:p>', '')
html = re.sub('mso-bookmark:_[A-Za-z0-9]*', '', html)

soup = BeautifulSoup(html, features="lxml")


def any_in(x, y):

    for a in x:
        if a in y:
            #print("%s in %s" % (a, x))
            return True

    return False



for match in soup.find_all(text=re.compile('^\xa0$')):
    match.parent.unwrap()

# Remove all span/style information except for colour if not black.

for match in soup.find_all('span', {"style" : True}):
    remaining_style = []
    is_code = False
    match['style'].replace("&quot;", '"')
    if not len(match['style']):
        match.unwrap()
        continue

    for style in match['style'].split(';'):
        #print(style)
        #try:
        key, value = style.split(':')
        # except:
        #    key = ""
        #    value = ""
        #    print("  BROKEN: %s" % (match))

        if key == "font-family":
            fonts = value.split(',')
            fonts = [x.lower() for x in fonts]
            fonts = [x.replace('"', '') for x in fonts]
            fonts = [x.strip() for x in fonts]
            #print("    %s" % fonts)

            fixed_fonts = ["courier new", "consolas"]

            if any_in(fixed_fonts, fonts):
                #print("HAVE CODE")
                is_code = True

        if key == "color":
            if value not in ['black']:
                remaining_style.append(style)

    if is_code:
        # TODO smarter about this
        # eg simpliy <o:p></o:p>
        #print("Have code")
        #print(match)
        match.wrap(soup.new_tag("pre"))
        match.unwrap()
        continue

    match['style'] = ";".join(remaining_style)







            





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

print(soup.prettify(formatter="html"))

