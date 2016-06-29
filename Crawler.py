import urllib.request

from html.parser import HTMLParser
from html.entities import name2codepoint

list_of_links = []

global markingSign
markingSign = 0


class MyHTMLParser(HTMLParser):
    def error(self, message):
        pass

    def handle_starttag(self, tag, attrs):
        global markingSign

        if tag == "a":

            if markingSign == 1:
                print("link: len: %d, span attrs: %s" % (len(attrs), attrs))
                print("link:", attrs[1][1])

                new_link = attrs[1][1]
                markingSign = 0
                # recursive calling of this function in order to get next pages
                parser = MyHTMLParser()
                with urllib.request.urlopen(new_link) as response:
                    html = response.read()
                    parser.feed(html.decode('utf-8'))

            elif len(attrs) > 2:
                if "linkWithHash" in attrs[0][1]:
                    list_of_links.append(attrs[1][1])

        elif tag == "span":
            if len(attrs) >= 1:
                if "fbold next" in attrs[0][1]:
                    markingSign = 1
                    print("len: %d, span attrs: %s" % (len(attrs), attrs))

link = 'http://olx.pl/motoryzacja/samochody/warszawa/?search%5Bfilter_float_price%3Ato%5D=7000&search%5Bfilter_float_price%3Afrom%5D=2500&search%5Bfilter_float_year%3Afrom%5D=1999&search%5Bfilter_enum_petrol%5D%5B0%5D=lpg&search%5Bfilter_enum_car_body%5D%5B0%5D=sedan&search%5Bfilter_enum_condition%5D%5B0%5D=notdamaged&search%5Bdist%5D=100&page=1'

parser = MyHTMLParser()
with urllib.request.urlopen(link) as response:
    html = response.read()
    parser.feed(html.decode('utf-8'))

for e in list_of_links:
    print(e)

print("count: ", len(list_of_links))
