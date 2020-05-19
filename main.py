from urllib.request import urlopen
from urllib.request import Request
from bs4 import BeautifulSoup as soup
import pandas as pd
import json
import requests
import argparse
import os.path
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

def getColumnData(itemsData,index):
    """
    Paramaters:
    --------------
    itemsData: list of list containing items data
    index: index of column you want to make

    Returns:
    list which represents the column of a particular item
    """
    return [itemsData[i][index] for i in range(len(itemsData))]

def createDataFrame(itemsData:list):
    """
    Parameters:
    --------------------
    
    itemsData: list of lists containing the items data
    
    Function: Combine the lists into one pandas dataframe object
    
    Returns:
    -------------------
    panda dataframe containing all item data

    """
    keys = ['Name','Model','Color','Brand','Release Date','Low Price','High Price','Currency']
    values = [getColumnData(itemsData,i) for i in range(len(itemsData[0]))]
    return pd.DataFrame({keys[i]:values[i] for i in range(len(keys))})

def scrapeHTML(html):
    """"
    Parameters:
    ----------------
    html: raw html page txt
    Function: scrapes the page and returns a pandas dataframe containing the item data
    Returns:
    ----------------
    pandas dataframe of the given html page
    """
    json_container = html.find_all("script",type="application/ld+json")
    data = ''
    for conatiner in json_container:
        data = json.loads(conatiner.string.extract())
        if(data['@type'] == 'OfferCatalog'):
            break
    items = data['itemListElement']
    itemsData = [getItemData(item) for item in items]
    df = createDataFrame(itemsData)
    return df

def scrapePages(startPage,endPage):
    """
    Parameters:
    ---------------
    startPage: specifies what page to start scraping from
    endPage: specifies what page to end scraping at

    Retunrs:
    -------------
    pandas dataframe containing all item data of products from startPage to endPage
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    base_url = 'https://stockx.com/sneakers?page='
    frames = []
    for i in range(startPage,endPage):
        currentPage = base_url + str(i)
        html = requests.get(currentPage).content
        currentPageDF = scrapeHTML(html)
        frames.append(currentPageDF)
    return pd.concat(frames,axis=0)

def main():
    parser = argparse.ArgumentParser(description='Shoe Scrapper for https://stockx.com/')

    parser.add_argument('--start',type=int,help='Starting index of page you want to scrape from.',required=True)
    parser.add_argument('--end',type=int,help='End index of page you want to scrape to.',required=True)
    parser.add_argument('--o',type=str,help='Location of the output file you want to store your scraped results.(MUST BE CSV)',required=True)
    
    args = parser.parse_args()

    df = scrapePages(args.start,args.end)
    if(os.path.isfile(args.o)):
        df.to_csv(args.o,mode='a',header=False)
    else:
        df.to_csv(args.o)
if __name__ == "__main__":
    main()