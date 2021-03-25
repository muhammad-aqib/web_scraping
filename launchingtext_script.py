from bs4 import BeautifulSoup
import requests
import pandas as pd

saas_app_list = []

url = 'https://www.launchingnext.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

items = soup.find_all('div', class_='preview')

for item in items:
    item_dict = {}
    item_dict['app_name'] = item.find('h3').text.strip()
    item_dict['url'] = item.find('a')['href']
    saas_app_list.append(item_dict)

next_key = soup.find('li', class_='next').find('a')['href']

count = 0
condition = 0

while(condition < 24000):
    url = 'https://www.launchingnext.com'+next_key
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')

    items = soup.find_all('div', class_='preview')

    for item in items:
        item_dict = {}
        item_dict['app_name'] = item.find('h3').text.strip()
        item_dict['url'] = item.find('a')['href']
        saas_app_list.append(item_dict)

    next_key = soup.find('li', class_='next').find('a')['href']
    condition = int(next_key[1:-1])
    count = count + 1

app_name = []
urls_list = []

for saas_app in saas_app_list:
    app_name.append(saas_app['app_name'])
    urls_list.append(saas_app['url'])

df_data = {
    'saas_directory': 'launchingnext',
    'app_name': app_name,
    'url': urls_list
}

df = pd.DataFrame(df_data, columns=['saas_directory', 'app_name', 'url'])

df.to_csv('./launchingtext.csv')

print(count)
print(len(saas_app_list))