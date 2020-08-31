import os
import csv
import requests
from bs4 import BeautifulSoup
os.system("clear")
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'}

def get_last_page(url):
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    soup.find('div')
    try:
        last_page = math.ceil(int(soup.find('p',{'class':'jobCount'}).find('strong').text.replace(',',''))/50)
    except:
        last_page = math.ceil(int(soup.find('p',{'class':'listCount'}).find('strong').text.replace(',',''))/50)
    return last_page

def get_job_info(url):
    last_page =get_last_page(url)
    temp =[]
    for i in range(last_page):
        page = url + f'?page={i+1}'
        print(page," 페이지 처리 중...")
        soup = BeautifulSoup(requests.get(page, headers=headers).content, 'html.parser').find('div', id = 'NormalInfo')
        soup = soup.find('tbody')
        for div in soup.find_all("tr", {'class':'summaryView'}):
            div.decompose()
        lists = soup.find_all("tr")

        for list in lists:
            place = list.find('td',{'class':'local'}).text.replace(u'\xa0',u' ').strip()
            title = list.find('span',{'class':'company'}).text.strip()
            try:
                time = list.find('span',{'class':'time'}).text.strip()
            except:
                time = list.find('span',{'class':'consult'}).text.strip()
            pay = list.find('td',{'class':'pay'}).text.strip()
            date = list.find('td',{'class':'regDate'}).text.strip()
            dic = {'place':place,'title':title,'time':time,'pay':pay,'date':date}
            temp.append(dic)
    return temp

def save_to_file(jobs,filename):
    file = open(f"{filename}.csv", mode='w', encoding='utf8',newline='')
    writer = csv.writer(file)
    writer.writerow(['place','title','time','pay','date'])
    for job in jobs:
        writer.writerow(list(job.values()))

url = 'http://www.alba.co.kr/'
soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
soup = soup.find('div',id='MainSuperBrand')
soup = soup.find('ul',{'class':'goodsBox'})

link_list = soup.find_all('li')

for link in link_list:
    company = link.find('span',{'class':'company'}).text
    lnk = link.find('a')['href']
    print(company," 에 대한 정보를 가져오고 있습니다.")
    result = get_job_info(lnk)
    save_to_file(result,company)
