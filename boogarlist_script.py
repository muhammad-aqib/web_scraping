from bs4 import BeautifulSoup
import requests
import pandas as pd

final_list_apps=[]
all_links=[]

sub_url_dict = {
    'Directory': 'http://www.boogar.com/resources/index.htm',
    'Conference': 'http://www.boogar.com/resources/conferences/calendar_september.htm',
    'Venture Capital': 'http://www.boogar.com/resources/venturecapital/alpha.htm'
    }

url = sub_url_dict['Directory']
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

items = soup.find('table', {"id": "table75"})

links = items.find_all('a',class_='LinkResourcesNav')

for link in links:
    all_links.append(link['href'])

for my_link in all_links:

        link_prefix = my_link.split('/')[0]

        saas_item_dict={}

        forward_link = sub_url_dict['Directory'].replace('index.htm',my_link)  
        response = requests.get(forward_link)
        soup = BeautifulSoup(response.text, 'lxml')
        page_anchors = soup.find_all('span', attrs={'style': 'font-size: 6.5pt'})
        
        try:
            pagination_list = page_anchors[2].find_all('a')
        except:
            pass
        
        saas_list=soup.find_all('td', attrs={'colspan': '2'})

        for saas_item in saas_list:
            try:
                final_list_apps.append([saas_item.find('a').text.strip(),saas_item.find('a')['href']])
            except:
                pass
    
        print(forward_link)

        for page in pagination_list:
            forward_link = sub_url_dict['Directory'].replace('index.htm',link_prefix+'/'+page['href'])  
            response = requests.get(forward_link)
            soup = BeautifulSoup(response.text, 'lxml')

            saas_list=soup.find_all('td', attrs={'colspan': '2'})
        
            for saas_item in saas_list:
                try:
                    final_list_apps.append([saas_item.find('a').text.strip(),saas_item.find('a')['href']])
                except:
                    pass

app_name = []
urls_list = []

for saas_app in final_list_apps:
    app_name.append(saas_app[0])
    urls_list.append(saas_app[1])


df_data = {
    'saas_directory': 'boogarlist',
    'app_name': app_name,
    'url': urls_list
}

df = pd.DataFrame(df_data, columns=['saas_directory', 'app_name', 'url'])

df.to_csv('./boogarlist22.csv',index=False)