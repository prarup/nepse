import os
import pandas as pd
import json
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
path  = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(path)
contentlist = []
with open('./data.json', 'r') as f:
  data = json.load(f)

for j in range(0,len(data)):
  driver.get(data[j])
  contentlist.clear()

  
  try:
    companyname = driver.find_element(By.XPATH,'/html/body/app-root/div/main/div/app-company-details/main/div/div[1]/div/div[2]/h1').text
  except:
    companyname = 'None'
  time.sleep(1)

  pricehistory = driver.find_element(By.XPATH, '//*[@id="pricehistory-tab"]')
  pricehistory.click()
  time.sleep(2)
  for y in range(1,7):
    time.sleep(2)
    for i in range(1,11):
      #sn = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[1]')
      try:
        date = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[2]').text 
      except:
        date = 'none'   
      try:                          
        openprice = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[3]').text
      except:
        openprice = 'none'
      try:
        highprice = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[4]').text
      except:
        highprice='none'
      try:
        lowprice = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[5]').text
      except:
        lowprice = 'none'
      
      try:
        closeprice = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[6]').text
      except:
        closeprice = 'none'
      try:
        ttq = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[7]').text
      except:
        ttq = 'none'
      try:
        tt = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[8]').text
      except:
        tt='none'
      try:
        prclosing = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[9]').text
      except:
        prclosing = 'none'
      try:
        fiftytwoweekhigh = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[10]').text
      except:
        fiftytwoweekhigh='none'
      try:
        fiftytwoweeklow = driver.find_element(By.XPATH, f'//*[@id="pricehistorys"]/div[1]/table/tbody/tr[{i}]/td[11]').text
      except:
        fiftytwoweeklow = 'none'
      
      contentlist.append({
        #'sn':sn.text,
        'date':date,
        'openprice':openprice,
        'highprice':highprice,
        'lowprice':lowprice,
        'closeprice':closeprice,
        'ttq':ttq,
        'tt':tt,
        'prclosing':prclosing,
        'fiftytwoweekhigh':fiftytwoweekhigh,
        'fiftytwoweeklow':fiftytwoweeklow
      })
    next = driver.find_element(By.XPATH, '//*[@id="pricehistorys"]/div[2]/pagination-controls/pagination-template/ul/li[9]')                                                            
    next.click()

  with open(f'pricehistory/{companyname}.json', 'w') as outfile:
    json.dump(contentlist,outfile)
driver.close()
