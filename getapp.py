def scrape_getapp():

    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    from csv import writer

    from selenium.webdriver.chrome.options import Options
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    page_url = 'https://www.getapp.com'
    all_the_apps = []

    driver = webdriver.Chrome('/Users/muhammadaqib/Downloads/chromedriver',options=chrome_options)
    driver.get(page_url)

    soup = BeautifulSoup(driver.page_source,'lxml')
    all_software_by_categories = soup.find('div',{'class':'container pb-4 mb-5 d-none d-lg-block'})
    categories = all_software_by_categories.find_all('div',{'class':'col-12 col-lg-6 categories-breakdown-col'})

    category_list=[]
    for category in categories:
        for item in category.find_all('div',{'class':'row no-gutters'}):
            category_list.append(item)

    len(category_list)

    final_list = []

    for item in category_list:
        for iterate in item.find_all('div',{'class':'d-flex align-items-center mb-2 pb-1 categories-breakdown-category'}):
            final_list.append([item.find('a').text,
                            page_url + iterate.find('a')['href']])

    print(len(final_list))

    for single_item in final_list:
        driver.get(single_item[1])
        soup = BeautifulSoup(driver.page_source,'lxml')
        
        try:
            page_num = int(soup.find('a',{'class':'pagination-item d-flex justify-content-center align-items-center ml-3 evnt'})['href'].split('/')[-2].split('-')[1]) + 1
        except:
            page_num = 2
        
        for i in range(1,page_num):
            
            url = single_item[1] + 'page-' + str(i)
            print('page_url *****',url)
            driver.get(url)
            soup = BeautifulSoup(driver.page_source,'lxml')
        
            apps_on_page = soup.find('div',{'class':'serp-listings'}).find_all('div','listing')
            for single_app in apps_on_page:
                driver.get(page_url + single_app.find('a','serp-read-more')['href'])
                soup = BeautifulSoup(driver.page_source,'lxml')

                try:
                    app_name = soup.find('h2',{'class':'cut'}).text
                except:
                    app_name=''

                app_category = single_item[0]
                
                try:
                    check_div = soup.find('div',{'class':'col-lg-8 col-md-8'})
                    
                    if(check_div.find('span',{'class':'text-muted'})):
                        domain = check_div.find('span',{'class':'text-muted'}).text.strip()
                    else:
                        domain = check_div.find('a',{'class':'text-muted'}).text.strip()

                except:
                    domain=''

                try:
                    description = soup.find('div',{'itemprop':'description'}).text.strip()
                except:
                    description = soup.find('div',{'class':'col-lg-10 col-md-10 col-sm-10 col-xs-9 listing-overview'}).find('p').text.strip()

                try:
                    business_sizes = soup.find('div',{'class':'business-sizes'})
                    item_business_size=[]
                    for b_size in business_sizes:
                        if 'active' in b_size['class']:
                            item_business_size.append(b_size['title'])
                    item_business_size = ' '.join(item_business_size).strip()

                except:
                    item_business_size=''

                try:
                    market = soup.find_all('div',{'style':'font-size:14px;'})[0].text.strip()
                except:
                    market = ''

                try:
                    lang = soup.find_all('div',{'style':'font-size:14px;'})[1].text.strip()
                except:
                    lang = ''
                try:
                    ratings = soup.find('div','review-summary-rating').text.strip()
                except:
                    ratings = ''

                item = ['getapp',app_name,app_category,domain,description,item_business_size,market,lang,ratings]
                print(item)
                with open('./getapp.csv', 'a') as f_object: 
                    
                    writer_object = writer(f_object) 
                    writer_object.writerow(item) 
                
                all_the_apps.append(item)
                print(len(all_the_apps))


    driver.close()

def create_getapp_csv():
    import csv

    with open('./getapp.csv', mode='w') as csv_file:
        fieldnames = ['saas_dir','app_name','app_category','domain','description','item_business_size','market','lang','ratings']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

# create_getapp_csv()
scrape_getapp()