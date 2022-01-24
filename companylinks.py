import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By

path  = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)

url = 'https://www.nepalstock.com.np/company'
driver.get(url)
time.sleep(2)
filter = driver.find_element(By.XPATH, '/html/body/app-root/div/main/div/app-company/div/div[2]/div/div[5]/div/select')
filter.send_keys('500')
button = driver.find_element(By.XPATH,'/html/body/app-root/div/main/div/app-company/div/div[2]/div/div[6]/button[1]')
button.click()
time.sleep(2)

content_list = []
try:
    for y in range(1,194):
        row = driver.find_elements(By.XPATH, f'/html/body/app-root/div/main/div/app-company/div/div[3]/table/tbody/tr[{y}]')
        for details in row:
            link = details.find_element(By.XPATH, f'/html/body/app-root/div/main/div/app-company/div/div[3]/table/tbody/tr[{y}]/td[2]/a').get_attribute('href')
        
            print('Loading')
            content_list.append(link)
    jstr = json.dumps(content_list)
    with open('data.json', 'w') as outfile:
            json.dump(content_list,outfile)
except:
    print('error')
driver.close()