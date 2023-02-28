import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from app import engine, Post, Products, Productstore, Productstorespec

def getHtmlText(link):
    header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36" ,
    'referer':'https://www.google.com/'
    }
    return requests.get(link ,headers=header).text

def scrapeEmag(link):
    #get the data from the products from the website
    html_text = getHtmlText(link)
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', class_ = "card-item card-standard js-product-data")

    #get the specifications of the products and store them into database
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    for product in products:
        productname1 = product.find('a', class_ = "card-v2-title semibold mrg-btm-xxs js-product-url").text.replace("  ", "")
        image1 = product.find('img')["src"]
        price = int(product.find('p', class_ = "product-new-price").text.replace(" лв", "").replace(".", "").replace(",", "").replace(".", "").replace("от ", ""))
        st1 = f'{(price%100):02}'

        new_product = Productstore(store = "emag", productname = productname1, imagesrc = image1, lev = price//100, st = st1)
        exist = sessiondb.query(Productstore).filter_by(productname = new_product.productname).first()
        
        #see if product already exists in the database if it exists check if the price have changed
        #if the product has changed its price with more than 10 lower change the price and add sale price
        #if the product has changed its price with higher change the price and don`t add sale
        if exist:
            if exist.lev != new_product.lev:
                razlika = int(exist.lev) - int(new_product.lev)
                if razlika > 10:
                    exist.levsale = new_product.lev
                    exist.stsale = new_product.st
                else:
                    exist.lev = new_product.lev
                    exist.st = new_product.st
                    exist.levsale = None
                    exist.stsale = None
                sessiondb.commit()
        else:
            sessiondb.add(new_product)
            sessiondb.commit()

def scrapeTechnopolis(link):
    Session = sessionmaker(bind=engine)
    sessiondb = Session()
    html_text = getHtmlText(link)
    soup = BeautifulSoup(html_text, 'lxml')
    products = soup.find_all('div', class_ = "product-box js-product__box")

    #get the specifications of the products and store them into database
    for product in products:
        productname1 = product.find('a', class_ = "product-box__title-link").text.replace("  ", "")
        price = int(product.find('span', class_ = "product-box__price-value").text.replace(" лв", "").replace(".", "").replace(",", "").replace(".", "").replace(" ", ""))
        st1 = str(product.find('sup').text)

        new_product = Productstore(store = "technopolis", productname = productname1, lev = price, st = st1)
        exist = sessiondb.query(Productstore).filter_by(productname = new_product.productname).first()
        
        if exist:
            if exist.lev != new_product.lev:
                razlika = int(exist.lev) - int(new_product.lev)
                if razlika > 10:
                    exist.levsale = new_product.lev
                    exist.stsale = new_product.st
                else:
                    exist.lev = new_product.lev
                    exist.st = new_product.st
                    exist.levsale = None
                    exist.stsale = None
                sessiondb.commit()
        else:
            sessiondb.add(new_product)
            sessiondb.commit()
