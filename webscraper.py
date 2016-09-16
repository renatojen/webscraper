"""
* 
* webscraper.py
* Author:
* Renato Jensen Filho
* 2016-09-15
* 
"""

import pandas
import requests
from bs4 import BeautifulSoup

base_url="http://pythonhow.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
headers = {'user-agent': 'Mozilla/5.0'} #define user agent
r=requests.get(base_url + '0' + ".html", headers) #use the first page to get the number of pages
c=r.content
soup=BeautifulSoup(c, "html.parser")
page_nr=soup.find_all("a", {"class": "Page"})[-1].text #get the number of pages
l=[]
for page in range(0, int(page_nr)*10, 10):
    if page != 0: #skips the steps below for the first page because we did them earlier
        r=requests.get(base_url + str(page) + ".html", headers)
        c=r.content
        soup=BeautifulSoup(c, "html.parser")
    
    all=soup.find_all("div", {"class" : "propertyRow"})

    for item in all:
        d={}
        try:
            d["Address"]=item.find_all("span", {"class" : "propAddressCollapse"})[0].text
        except:
            d["Address"]=None
        try:
            d["Locality"]=item.find_all("span", {"class" : "propAddressCollapse"})[1].text
        except:
            d["Locality"]=None
        try:
            d["Price"]=item.find("h4", {"class" : "propPrice"}).text.replace('\n', "").replace(" ", "")
        except:
            d["Price"]=None
        try:
            d["Beds"]=item.find("span", {"class" : "infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span", {"class" : "infoSqFt"}).find("b").text
        except:
            d["Area"]=None
        try:
            d["Full Baths"]=item.find("span", {"class" : "infoValueFullBath"}).find("b").text
        except:
            d["Full Baths"]=None
        try:
            d["Half Beds"]=item.find("span", {"class" : "infoValueHalfBath"}).find("b").text
        except:
            d["Half Beds"]=None
        for column_group in item.find_all("div", {"class" : "columnGroup"}):
            for feature_group, feature_name in zip(column_group.find_all("span", {"class" : "featureGroup"}), column_group.find_all("span", {"class" : "featureName"})):
                if "Lot Size" in feature_group.text:
                    try:
                        d["Lot Size"]=feature_name.text        
                    except:
                        d["Lot Size"]=None
        l.append(d)

df = pandas.DataFrame(l)
df.to_csv("output.csv")