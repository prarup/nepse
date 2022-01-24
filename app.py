import json
import pandas as pd
from bs4 import BeautifulSoup
import requests
from flask import Flask ,request,render_template
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

c = DesiredCapabilities.CHROME
c["pageLoadStrategy"] = "none"

app = Flask(__name__)

productdict=[]
productlinks =[]
imagelinks =[]
jstr = []

@app.route("/")
def home():
    productdict.clear()
    productlinks.clear()
    imagelinks.clear()
    jstr.clear()
    return render_template('index.html')

@app.route("/rej/",methods=['POST', 'GET'])
def products():
    driver = webdriver.Chrome(executable_path="C:\Program Files (x86)\chromedriver.exe", desired_capabilities=c)
    w = WebDriverWait(driver, 15)
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    
    category =  request.form.get("category")
    page_no =  int(request.form.get("page_no"))

    try:
        for i in range (1,2):
            url = f'https://www.alibaba.com/products/{category}.html?IndexArea=product_en&page={i}'
            driver.get(url)
            w.until(EC.presence_of_element_located((By.CLASS_NAME, 'elements-title-normal__below')))
            time.sleep(2)
            driver.execute_script("window.stop();")
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(5)
            contents = driver.find_elements(By.CSS_SELECTOR , '.img-switcher-parent')

            for content in contents:
                    try:
                        productlink = content.find_element(By.TAG_NAME,'a').get_attribute('href')
                    except:
                        productlink = 'none'
                    try:
                        image_link = content.find_element(By.CLASS_NAME, 'seb-img-switcher__imgs').get_attribute('data-image')
                    except:
                        image_link= 'none' 

                    productlinks.append(productlink)
                    imagelinks.append(image_link)

        driver.close()
        
        for p in range(1, len(productlinks)): 
            r = requests.get(productlinks[p])
            soup = BeautifulSoup(r.content, 'lxml')

            try:
                pname = soup.find('h1', class_='module-pdp-title').text
            except: 
                pname = 'none'
            try:
                pprice = soup.find('span', class_='pre-inquiry-price').text
            except:
                pprice = 'none'
            try:
                script = soup.find_all('script')[25].text.strip()[139:]
                data = json.loads(script)
                details= data['globalData']['product']['productBasicProperties']
            except:
                details = 'none'
 
            print(pname)
            productdict.append({
                                'ProductName': pname,
                                'ProductPrice': pprice,
                                'ImageLink':imagelinks[p],
                                'ProductLinks': productlinks[p],
                                'Details': details
                                            })
                    
        jstr =json.dumps(productdict)  
        
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")

        with open(f'{category}.json', 'w') as outfile:
            json.dump(productdict,outfile)

        df = pd.read_json(f'./{category}.json')
        df.to_excel(f'./{category}.xlsx')         
        return render_template('rej.html', json_dump= jstr)
    
    except:
        print('error')
    
@app.route("/rej/",methods=['GET'])
def results():
    jstr = json.dumps(productdict)
    return render_template('rej.html', json_dump=jstr, Headers = None)

if __name__ == "__main__":
    app.run(port=80)