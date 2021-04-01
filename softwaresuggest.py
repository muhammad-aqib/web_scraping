def scrape_directory():

    from selenium import webdriver
    from bs4 import BeautifulSoup
    import pandas as pd
    from csv import writer
    import time
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver import ActionChains
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    url = 'https://www.softwaresuggest.com/all-categories'
    all_the_apps=[]

    driver = webdriver.Chrome('/Users/muhammadaqib/Downloads/chromedriver')
    driver.get(url)

    soup = BeautifulSoup(driver.page_source,'lxml')

    all_categories = soup.find('div','mdl-grid compare_row').find_all('a')

    category_list=[]
    for category in all_categories:
        category_list.append([category.text.strip(),category['href']])


    for item in category_list:
        driver.get(item[1])
        print('url***', item[1])
        soup = BeautifulSoup(driver.page_source,'lxml')
        try:
            check_pager = soup.find('ul',{'id':'mypager_id'})
        except:
            check_pager = None
        try:
            check_more_button = soup.find('button',{'class':'ga_track_vmp_lmb cat_view_more_btn ripple_btn'})
        except:
            check_more_button = None
        
        if check_pager:
            last_page = check_pager.find_all('li')[-1].find('a')['href'].split('?')[-1].split('=')[-1]
            for pg_no in range(1,int(last_page)+1):
                print(item[1] + '?page=' + str(pg_no))
                driver.get(item[1] + '?page=' + str(pg_no))
                soup = BeautifulSoup(driver.page_source,'lxml')
                
                apps_on_page = soup.find('div','cat_list_append').find_all('h3','slist_oftware_name')
                for app_item in apps_on_page:
                    try:
                        driver.get(app_item.find('a')['href'])
                    except:
                        app_url = app_item.find('span','d-flex align-items-center ga_track_soft_name new_link_onclick')['onclick'].split('(')[1][1:-11]
                        driver.get(app_url)
                    soup = BeautifulSoup(driver.page_source,'lxml')

                    print(app_item.text.strip())
                    title = app_item.text.strip()
                    category  = item[0]
                    try:
                        find_app_url = soup.find('span','ga_track_vwl_comp_d comp_detail_vwb_btn cursor_pointer')['onclick']
                        driver.get(find_app_url.split('(')[1][1:-11])
                        time.sleep(5)
                        url = driver.current_url
                    except:
                        url = driver.current_url
                    url = url.split('/')[2]
                    
                    print(['pagination',title,category,url])
                    app_info = ['softwaresuggest',title,category,url]
                    with open('/Users/muhammadaqib/Documents/softwaresuggest.csv', 'a') as f_object: 

                        writer_object = writer(f_object) 
                        writer_object.writerow(app_info) 

                    all_the_apps.append(app_info)
                    print(len(all_the_apps))
                    

        if check_more_button:
            print('CHECK MORE BUTTON')
            while check_more_button:
                try:
                    wait = WebDriverWait(driver, 10)
                    accept = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="cat_list_tab_1"]/div[3]/button')))

                    actions = ActionChains(driver)
                    actions.move_to_element(accept).click().perform()
                except:
                    break
            
            soup = BeautifulSoup(driver.page_source,'lxml')
                
            apps_on_page = soup.find('div','cat_list_append').find_all('h3','slist_oftware_name')
            for app_item in apps_on_page:
                try:
                    driver.get(app_item.find('a')['href'])
                except:
                    app_url = app_item.find('span','d-flex align-items-center ga_track_soft_name new_link_onclick')['onclick'].split('(')[1][1:-11]
                    driver.get(app_url)
                soup = BeautifulSoup(driver.page_source,'lxml')
                
                print(app_item.text.strip())
                title = app_item.text.strip()
                category  = item[0]
                try:
                    find_app_url = soup.find('span','ga_track_vwl_comp_d comp_detail_vwb_btn cursor_pointer')['onclick']
                    driver.get(find_app_url.split('(')[1][1:-11])
                    time.sleep(5)
                    url = driver.current_url
                except:
                    url = driver.current_url
                url = url.split('/')[2]        
                print(['check more button',title,category,url])
                app_info = ['softwaresuggest',title,category,url]

                with open('/Users/muhammadaqib/Documents/softwaresuggest.csv', 'a') as f_object: 
                    writer_object = writer(f_object) 
                    writer_object.writerow(app_info) 

                all_the_apps.append(app_info)
                print(len(all_the_apps))

    driver.close()


def create_softwaresuggest_csv():
    import csv

    with open('/Users/muhammadaqib/Documents/softwaresuggest.csv', mode='w') as csv_file:
        fieldnames = ['saas_dir','app_name','app_category','domain']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
    