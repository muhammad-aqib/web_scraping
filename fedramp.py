from selenium import webdriver  
from bs4 import BeautifulSoup   
import pandas as pd

page_url = 'https://marketplace.fedramp.gov/#!/products?sort=productName'   
driver = webdriver.Chrome('/Users/muhammadaqib/Downloads/chromedriver')   
driver.get(page_url)    
driver.implicitly_wait(10)

all_apps=[] 
xpath_list=[]

for i in range(1,304):
    xpath_list.append('//*[@id="products-grid"]/div[2]/tile[{}]/div/div/div/div[1]/a'.format(str(i)))

for xpath in xpath_list:
    driver.find_element_by_xpath(xpath).click()
    soup = BeautifulSoup(driver.page_source,'lxml') 
    product_info = soup.find('div',{'class':'information product'}) 
    
    try:
        saas_name = product_info.find('div',{'class':'title'}).text.strip() 
    except:
        saas_name=''
        
    try:
        saas_url = product_info.find('a',{'title':'Visit the provider website'})['href'].strip()
    except:
        saas_url=''
        
    all_apps.append(['fedramp',saas_name,saas_url]) 
    driver.get(page_url)

driver.close()  

item_cols = ['saas_dir','app_name','url']
items_df = pd.DataFrame(all_apps, columns=item_cols)
items_df.to_csv('./fedramp.csv', index=False) 

    
