from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

#Amazon URL
url = 'https://www.amazon.com/s?k={}&ref=nb_sb_noss'
search_query='ultrawide monitor'
last_page=20
final_items_list=[]


def get_url(search_term):
    search_term = search_term.replace(' ','+')
    final_url = url.format(search_term)
    final_url = final_url + '&page={}'
    return final_url


def get_product_url(item):
    product_url = item.find('a',{'class':'a-link-normal a-text-normal'})['href'] if item.find('a',{'class':'a-link-normal a-text-normal'}) else ''
    return 'https://amazon.com' + product_url


def extract_item(page_number):
    print(page_number)
    driver.get(get_url(search_query).format(str(page_number)))
    soup = BeautifulSoup(driver.page_source,'lxml')
    all_items = soup.find_all('div','s-include-content-margin s-border-bottom s-latency-cf-section')
    
    for item in all_items:
            item_name = item.find('span',{'class':'a-size-medium a-color-base a-text-normal','dir':'auto'}).text.strip() \
                 if item.find('span',{'class':'a-size-medium a-color-base a-text-normal','dir':'auto'}) else ''
            
            item_price = item.find('span',{'class':'a-offscreen'}).text.strip() if item.find('span',{'class':'a-offscreen'}) else ''
            item_rating = item.find('span',{'class':'a-icon-alt'}).text.strip() if item.find('span',{'class':'a-icon-alt'}) else ''
            item_reviews = item.find('span',{'class':'a-size-base','dir':'auto'}).text.strip() if item.find('span',{'class':'a-size-base','dir':'auto'}) else ''
            
            product_url = get_product_url(item)

            final_items_list.append((item_name, item_price, item_rating, item_reviews, product_url))


driver = webdriver.Chrome()

for i in range(1,last_page+1):
    extract_item(i)

driver.close()

item_cols = ['item_name','item_price','item_rating','item_review','product_url']
items_df = pd.DataFrame(final_items_list, columns=item_cols)
items_df.to_csv('amazon_items.csv', index=False)