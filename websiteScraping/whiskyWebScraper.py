# import libraries
import urllib.request as urllib2
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pprint

# create a variable for url
baseUrl = 'https://www.thewhiskyexchange.com'

# create variable for user-agent
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}

# HTTP call 
# k = requests.get('https://www.thewhiskyexchange.com/c/33/american-whiskey').text

# Create empty list
productLinks = []
# beautiful soup extraction 
for x in range(1,13):
    k = requests.get('https://www.thewhiskyexchange.com/c/33/american-whiskey?pg={}&psize=24&sort=pasc'.format(x)).text # HTTP call
    soup = BeautifulSoup(k, 'html.parser') # parse html with BeautifulSoup
    productList = soup.find_all('li', {'class':'product-grid__item'}) # using bs4 to find data

    for product in productList: # create a for loop to obtain all prodcuts 
        link = product.find('a', {'class':'product-card'}).get('href')
        productLinks.append(baseUrl + link)
# print(productlinks)

# create empty list for data
data = []
# Extract data you want from each link using for loop
for link in productLinks:
    f = requests.get(link, headers=headers).text # call links 
    hun = BeautifulSoup(f, 'html.parser') # parse texts from links

    try:
        price = hun.find('p', {'class':'product-action__price'}).text.replace('/n', '')
    except:
        price = None

    try:
        about = hun.find('div', {'class':'product-main__description'}).text.replace('/n', '')
    except:
        about = None
    
    try:
        rating = hun.find('div', {'class':'review-overview'}).text.replace('/n', '')
    except:
        rating = None
    
    try:
        name = hun.find('h1', {'class':'product-main__name'}).text.replace('/n', '')
    except:
        name = None

    whisky = {'name':name, 'price':price, 'rating':rating, 'about':about}

    data.append(whisky)

df = pd.DataFrame(data)

