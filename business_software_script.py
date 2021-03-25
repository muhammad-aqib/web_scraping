from bs4 import BeautifulSoup
import pandas as pd
import requests

saas_apps_list=[]

for page_no in range(1,43):
    url='https://www.business-software.com/product-finder/?pager={}&count=100&sort=popular'.format(str(page_no))
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'lxml')
    all_items = soup.find('ul',{"id": "result-list"}).find_all('h3')

    for item in all_items:
        response = requests.get(item.find('a')['href'])
        soup = BeautifulSoup(response.text, 'lxml')
        try:
            app_name = soup.find('h1',{"id": "product-page-title"}).text.strip().replace(' Review','')
            product_url = soup.find('div',class_='gfe-product-snippet').find('a')['href'].strip()
            saas_apps_list.append([app_name,product_url])
        except:
            saas_apps_list.append([app_name,''])
        finally:
            print(saas_apps_list[-1],len(saas_apps_list),page_no)

app_name, urls_list = [(saas_app[0], saas_app[1]) for saas_app in saas_apps_list]

df_data = {
    'saas_directory': 'business_software',
    'app_name': app_name,
    'url': urls_list
}

df = pd.DataFrame(df_data, columns=['saas_directory', 'app_name', 'url'])
df.to_csv('./business_software_saas_apps.csv', index=False)