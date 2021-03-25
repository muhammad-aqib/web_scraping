from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

url = 'https://whotracks.me/'

app_item = []

response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
navbar_items = soup.find('ul',class_='nav navbar-nav navbar-right').find_all('li')

nav_urls = []

for url_item in navbar_items[:2]:
    final_url = url_item.find('a')['href'][2:]
    nav_urls.append(url + final_url)
    
trackers_url = nav_urls[0]
websites_url = nav_urls[1]

#TRACKERS URLS
response = requests.get(trackers_url)
soup = BeautifulSoup(response.text,'lxml')
app_list = soup.find('ul',{"id": "multi-column-list"}).find_all('li')

for app in app_list:
    domain_name = app.find('a').text
    
    app_item_url=url+app.find('a')['href'][2:]

    response = requests.get(app_item_url)
    soup = BeautifulSoup(response.text,'lxml')
    domains = soup.find('div',{'id':'operates-under'}).find_all('p')
    
    domain_list=[]
    for domain in domains:
        app_item.append([domain_name,domain.text.strip()])
        print('length of urls extracted {} ----- {}'.format(str(len(app_item)),app_item[-1]))
        

#WEBSITE URLS
response = requests.get(websites_url)
soup = BeautifulSoup(response.text,'lxml')
app_list = soup.find('ul',{"id": "multi-column-list"}).find_all('li')

for app in app_list:
    app_item.append([app.find('a').text,app.find('a').text])
    print('length of urls extracted {} ----- {}'.format(str(len(app_item)),app_item[-1]))

app_name_list=[]
urls_list=[]

for item in app_item:
    app_name_list.append(item[0])
    urls_list.append(item[1])

df_data = {
    'saas_directory': 'whotracksme',
    'app_name': app_name_list,
    'url': urls_list
}

df = pd.DataFrame(df_data, columns=['saas_directory', 'app_name', 'url'])
df.to_csv('./whotracksme.csv', index=False)


