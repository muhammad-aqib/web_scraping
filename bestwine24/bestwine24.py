from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import pandas as pd

page_url = "https://bestwine24.ru/vino/smf/tsvet-is-krasnoe/tsena-is-do-1000/?page={}"

all_items=[]

custom_options = webdriver.ChromeOptions()
custom_options.add_argument("--lang=en")
custom_options.add_argument("--disable-popup-blocking")

prefs = {
  "translate_whitelists": {"ru":"en"},
  "translate": {"enabled":"true"}
}

custom_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome('/Users/muhammadaqib/Downloads/chromedriver', options=custom_options)

driver.implicitly_wait(10)
driver.get(page_url.format(str(1)))

above18_button = driver.find_element_by_xpath('//*[@id="popup-1"]/div/div/div/div[3]/span')
above18_button.click()

for i in range(1,21):
    driver.get(page_url.format(str(i)))
    soup = BeautifulSoup(driver.page_source,'lxml')
    product_grid = soup.find('div','product-grid active')
    all_products = product_grid.find_all('div',{'data-type':'product'})
    
    for product in all_products:
        product_name = product.find('div','name').text
        
        description = product.find_all('div','value')
        
        try:
            wine_type = description[0].text.strip()
        except:
            wine_type=''
        try:
            flavor = description[1].text.strip()
        except:
            flavor = ''
        try:
            location = description[2].text.strip()
        except:
            location = ''
                  
        available_qty = product.find('span','status in').text.strip()
        print(product_name,available_qty)
        item = [product_name,wine_type,flavor,location,available_qty]
        
        all_items.append(item)
        
print(len(all_items))

driver.close()

item_cols = ['product_name','wine_type','flavor','location','available_qty']
items_df = pd.DataFrame(all_items, columns=item_cols)
items_df.to_csv('bestwine24.csv', index=False)
