import urllib.request
import OfferParser as op
from html.parser import HTMLParser
from html.entities import name2codepoint
from bs4 import BeautifulSoup
import urllib.request
from geopy.geocoders import Nominatim
import re
from bs4 import BeautifulSoup

list_of_links = []

global markingSign
markingSign = 0


def gather_data(link):
    with urllib.request.urlopen(link) as response:
        html = response.read()
    soup = BeautifulSoup(html, 'html.parser')

    nazwa = soup.find("div", {"class": "offerheadinner"}).h1.contents[0].strip()
    print(nazwa)

    miejsce = soup.find("span", {"class": "show-map-link link gray cpointer"}).strong.contents[0].strip()
    print(miejsce)

    geolocator = Nominatim()
    location = geolocator.geocode(miejsce)
    # print(location.address)
    print("latitude: ", location.latitude)
    print("longitude:", location.longitude)

    # dla normalnych:
    # datee = soup.find("span", {"class": "pdingleft10 brlefte5"}).contents[0].strip().replace("   ", "")
    # print(datee)

    # dla mobilek:
    # datee = soup.find("span", {"class": "pdingleft10 brlefte5"})

    datee = soup.find(string=re.compile(" o ")).replace("\n", "").replace("   ", "")
    print(datee)

    # print("datee = soup.find(span ", datee)
    # for e in datee:
    #     if "odano" in e:
    #         print(e)
    #     if len(e) > 5:
    #         data_dodania = e.string.strip()
    #         czysta_data_dodania = data_dodania.replace("   ", "")
    #         # print(e.string)
    #     else:
    #         czysta_data_dodania = "nie znaleziono daty"
    #
    # print("data dodania: ", czysta_data_dodania)

    id_field_of_searching = soup.find("span", {"class": "rel inlblk"})
    print("id: ", id_field_of_searching.string)
    #
    # id_field_of_searching = soup.find("span", {"class": "rel inlblk"})
    # print("id: ", id_field_of_searching.string)


    obrazek = soup.find("div", {"class": "photo-handler rel inlblk"}).img.get('src')
    print(obrazek)

    cena = soup.find("div", {"class": "pricelabel tcenter"}).strong.contents[0].strip()
    print(cena)

    data_tables = soup.find_all("table", {"class": "item"})
    # print(data_tables)


    for t in data_tables:
        label = t.find("th").contents[0].strip()
        if t.find("a") is not None:
            value = t.find("a").contents[0].strip()
        else:
            value = t.find("strong").contents[0].strip()
        print(" %s : %s" % (label, value))

    ops = soup.find("div", {"id": "textContent"})
    string_content = ops.get_text()
    print(string_content)

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
    print("calling offer parser with link: ", e)
    gather_data(e)
    # print(e)

print("count: ", len(list_of_links))
