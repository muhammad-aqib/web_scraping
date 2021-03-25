from bs4 import BeautifulSoup
import requests
import pandas
from datetime import datetime

job_list = []

def get_url(title, location):
    template='https://pk.indeed.com/jobs?q={}&l={}'
    return template.format(title.replace(' ','+'),location)

url = get_url('software engineer','karachi')


while True:
    page_html = requests.get(url).content
    soup = BeautifulSoup(page_html,'lxml')
    cards_list = soup.find_all('div',{'class':'jobsearch-SerpJobCard'})
    
    for card in cards_list:
        job_title = card.h2.a.get('title').strip() if card.h2.a.get('title') else ''
        company = card.find('span',{'class':'company'}).text.strip() if card.find('span',{'class':'company'}) else ''
        location = card.find('span', {'class':'location'}).text.strip() if card.find('span', {'class':'location'}) else ''
        job_summary = card.find('div',{'class':'summary'}).text.strip().replace('\n',' ') if card.find('div',{'class':'summary'}) else ''
        post_date = card.find('span',{'class':'date'}).text.strip() if card.find('span',{'class':'date'}) else ''
        today = datetime.today().strftime('%Y-%m-%d')
        
        job_list.append((job_title,company,location,job_summary,post_date,post_date,today))
        print(job_list[-1][0])
    
    try:
        url = 'https://pk.indeed.com'+soup.find('a',{'aria-label':'Next'}).get('href')
    except AttributeError: #When next button is gone.
        break


print(job_list)
        
        