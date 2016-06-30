import urllib.request
from geopy.geocoders import Nominatim
import re
from bs4 import BeautifulSoup


class OfferParser:
    'Common base class for all employees'
    empCount = 0

    def __init__(self, link):
        self.link = link
        self.gather_data(link)

    def gather_data(self, link):
        with urllib.request.urlopen(link) as response:
            html = response.read()
        soup = BeautifulSoup(html, 'html.parser')

        nazwa = soup.find("div", {"class": "offerheadinner"}).h1.contents[0].strip()
        print(nazwa)

        miejsce = soup.find("span", {"class": "show-map-link link gray cpointer"}).strong.contents[0].strip()
        print(miejsce)

        geolocator = Nominatim()
        location = geolocator.geocode(miejsce)
        print(location.address)
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


#link = "http://olx.pl/oferta/sprzedam-fiat-brava-1-6-CID5-IDgm4hx.html#72466d0039"
# link = "http://olx.pl/oferta/opel-vectra-b-lpg-brc-skora-irmscher-CID5-IDgm451.html#72466d0039"

#
# opis = soup.find_all("p", {"class": "pding10 lheight20 large"})
#
# print(opis)
