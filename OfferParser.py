import urllib.request
from geopy.geocoders import Nominatim

from bs4 import BeautifulSoup

link = "http://olx.pl/oferta/opel-vectra-2-2-z-gazem-i-klima-elektryka-CID5-IDgks9D.html#5aa27adc3e"

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
print((location.latitude, location.longitude))

data_dodania = soup.find("span", {"class": "pdingleft10 brlefte5"}).contents[0].strip()
print(data_dodania)

id_ogloszenia = soup.find("span", {"class": "pdingleft10 brlefte5"}).span.span.contents[0].strip()
print(id_ogloszenia)

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
    print(" %s : %s"%(label, value))

opis = soup.find_all("p", {"class": "pding10 lheight20 large"})

print(opis)

