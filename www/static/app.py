import urllib
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import os
import pandas as pd
from selenium.webdriver.chrome.options import Options
p1=[]
nopiclist=[]
finish=[]
df1=pd.DataFrame()
df2=pd.DataFrame()
failurl=[]
newurl=[]
secondurl=[]
successful=[]
# url=r'http://hk.centadata.com/FloorPlan.aspx?type=2&code=SSPPWPPYPS&ref=CD2_Detail'
# url=r'http://hk.centadata.com/FloorPlan.aspx?type=1&code=SSWYGPSJPS&ref=CD2_Detail'
p = os.walk(r'F:\中原外景图\url1')
ps = pd.read_excel(r'F:\已爬取物業1.xlsx').values
pa = pd.read_excel(r'F:\無平面圖物業1.xlsx').values
for ps_ in ps:
    ps_=ps_[0].replace('FloorPlan.aspx','ptest.aspx').replace('Detail','paddresssearch')
    newurl.append(ps_)
for pa_ in pa:
    pa_=pa_[0].replace('FloorPlan.aspx','ptest.aspx').replace('Detail','paddresssearch')
    newurl.append(pa_)
print(newurl)


for dirs,roots,files in p:
    for file in files:
        if 'xls' in file:
            p = os.path.join(dirs,file)
            p1.append(p)
for path in p1:
    print(path)
    filepath=path.split('\\')[-1].replace(".xlsx","")
    print(filepath)
    urls=pd.read_excel(path).values
    for url in urls:    
        url=url[0]
        df = pd.DataFrame()
        if 'paddresssearch' in url:
            if url not in newurl: 
                time.sleep(0.5)
                newurl.append(url)
                print(url)
                type=re.findall(u'type=\d',url)[0].replace("type=","")
                code=re.findall(u'code=[A-Z]+',url)[0].replace("code=","")
                url=r'http://hk.centadata.com/FloorPlan.aspx?type=%s&code=%s&ref=CD2_Detail'%(type,code)

                headers = {'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
                req = urllib.request.Request(url=url,headers=headers)
                content = urllib.request.urlopen(req,timeout=50).read()
                soup = BeautifulSoup(content,'html.parser')
                s = soup.find('div',class_='maptools_content_alert')
                if s is None:
                    name = soup.find(class_='building_title').text
                    print(filepath,"-",name)
                    yes = 'F:\\中原外景图\\'+filepath+'\\'+str(name)
                    isExists=os.path.exists(yes)
                    if not isExists:
                        finish.append(url)
                        successful.append(name)
                        df2=pd.DataFrame({'url':finish,'name':successful})
                        df2.to_excel(r'F:\已爬取物業.xlsx')
                        picweb =[]
                        buildname=[]
                        chrome_options = Options()
                        chrome_options.add_argument('--headless')
                        chrome_options.add_argument('--disable-gpu')
                        web_driver=webdriver.Chrome(r'C:\Users\Administrator\Downloads\chromedriver_win32\chromedriver.exe',chrome_options=chrome_options)
                        web_driver.get(url)
                        piclists=web_driver.find_elements_by_xpath('//div[@class="estate_list"]/table/tbody/tr/td')#取圖片名
                        for piclist in piclists:
                            picnum = piclist.text
                            print(picnum)
                            buildname.append(picnum)
                    else:
                        print('爬過了')
                        time.sleep(1)
                        continue
                else:
                    name = soup.find(class_='building_title').text
                    nopiclist.append(name)
                    failurl.append(url)
                    df1=pd.DataFrame({'url':failurl,'name':nopiclist})
                    df1.to_excel(r'F:\無平面圖物業.xlsx')
                    continue
                time.sleep(1)            
                picname=web_driver.find_elements_by_xpath('//div[@class="estate_list"]/table/tbody/tr/td/a')   
                for cli in picname:#取圖片地址
                    cli.click()
                    time.sleep(1)
                    picurl=web_driver.find_element_by_xpath('//div[@class="img_mask"]/div/a')
                    picurl=picurl.get_attribute('href')
                    print(picurl)
                    picweb.append(picurl)                                   
                    time.sleep(1)
                print(picweb)
                df = pd.DataFrame({'url':picweb,'name':buildname})
                picpath=str('F:\\中原外景图\\'+filepath+'\\'+str(name))
                isExists=os.path.exists(picpath)
                print(picpath)
                if not isExists:
                    os.makedirs(picpath)
                picpath2=str(picpath+'\\'+str(name)+'.xlsx')
                print(picpath2)
                df.to_excel(picpath2,index=None)
                web_driver.close()
            else:
                print('昨天爬了')
                continue
        else:
            continue