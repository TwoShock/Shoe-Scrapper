from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd
import json

def getItemData(item:dict)->list:
    """
    Parameters:
    -----------------------
    item:dictionary containing item data
    function: extracts the neccessary json data
    
    Returns:
    -------------------------
    a list containing all the relevant item data
    """

    brand = item['item']['brand']
    color = item['item']['color']
    model = item['item']['model']
    name = item['item']['name']
    releaseDate = item['item']['releaseDate']
    lowPrice = item['item']['offers']['lowPrice']
    highPrice = item['item']['offers']['lowPrice']
    currency = item['item']['offers']['priceCurrency']
    return [name,model,color,brand,releaseDate,lowPrice,highPrice,currency]

#def createDataFrame(itemData:list)->pandas:
def main():
    with open('index.html') as file:
       html = soup(file,'lxml')

    json_container = html.find_all("script",type="application/ld+json")
    data = json.loads(json_container[4].string.extract())
    
    items = data['itemListElement']
    itemsData = [getItemData(item) for item in items]


if __name__ == "__main__":
    main()