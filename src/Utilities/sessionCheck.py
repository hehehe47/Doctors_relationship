#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/11 17:52 
# @Author : Patrick 
# @File : sessionCheck.py
# @Software: PyCharm

import cfscrape
import requests
import bs4

HEADER = {
    # ':authority': 'www.vitals.com',
    # ':method': 'GET',
    # ':path': '/search/ajax?display_type=Doctor&reqNo=0',
    # ':scheme': 'https',
    'accept': '*/*',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    'cookie': '__cfduid=d209720f82a81815bb362300219b20e011573066924; _ga=GA1.2.2085121120.1573066926; __qca=P0-1607991460-1573066926294; _fbp=fb.1.1573066926831.1764652283; s_fid=002AAA10F5BFC56C-1D0C741AE37167AD; PHPSESSID=urg5anddfh4cfopcospobigt5d; s_cc=true; __cfruid=244bdf4b07c6b789d5326a3b785fd98966516c96-1573331444; _gid=GA1.2.965269268.1573331445; retarget=%5B%5D; _dc_gtm_UA-2543312-1=1; s_sq=webmdp1global%3D%2526c.%2526a.%2526activitymap.%2526page%253Dvitals.com%25252Fdoctors%2526link%253DSEARCH%252520%252526%252520FILTER%2526region%253DBODY%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dvitals.com%25252Fdoctors%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.vitals.com%25252Fsearch%25253Fdisplay_type%25253DDoctor%2526ot%253DA',
    'referer': 'https://www.vitals.com/search?display_type=Doctor',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest'
}

header = {
    # ':authority': 'www.sciencedirect.com',
    # ':method': 'GET',
    # ':path': '/science/article/pii/S1936879818301055',
    # ':scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    # 'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en,zh-CN;q=0.9,zh;q=0.8,zh-TW;q=0.7',
    'cache-control': 'max-age=0',
    'cookie': '__cfduid=da7859d5a9f12f23f997517e8cc75585a1574298897; EUID=2b584d70-4399-4eda-a65a-00ab0da1e618; sd_session_id=76710c7f481be346d09b2a14b4824956c3a2gxrqa; acw=76710c7f481be346d09b2a14b4824956c3a2gxrqa%7C%24%7C57B69F49FBEC8DDE0C2326798A9326E79703B63C17000A72CC8FEA6782974B4B2CF2882E797743A75B7962C8A198655806F418A6BF5C4B783FBA44D1BD4E4F2EAFE9C31A29ED2080B6DA1F7CB1786ABB; ANONRA_COOKIE=C1AAE7B1275E86A154F0608EDA3BF3A354461BAB6533394CAA0842CCB210034E19AC6F36081D3E899C724C17C7D9F42C050E56DE55D95C69; utt=f2b42f0646b8e61d56184b41209304cf52d1719-q; AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1; fingerPrintToken=9ff9e979c5550451e3cd6bdf75dbdab9; AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=-1712354808%7CMCIDTS%7C18222%7CMCMID%7C63145178096309998711457928473032304137%7CMCAAMLH-1574903700%7C7%7CMCAAMB-1574903700%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1574306100s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C1026065531%7CvVersion%7C4.3.0; SD_ART_LINK_STATE=%3Ce%3E%3Cq%3Escience%3C%2Fq%3E%3Corg%3Erslt_list%3C%2Forg%3E%3Cz%3Erslt_list_item%3C%2Fz%3E%3CsrcFr%3Erslt_list_item%3C%2FsrcFr%3E%3Crdt%3E2019%2F11%2F21%2F01%3A19%3A30%3A591%3C%2Frdt%3E%3Cenc%3EN%3C%2Fenc%3E%3C%2Fe%3E; MIAMISESSION=cb3b96e2-707d-4b91-98d4-eb36b5e4111c:3751751969; s_pers=%20c19%3Dsd%253Aproduct%253Ajournal%253Aarticle%7C1574300971440%3B%20v68%3D1574299169826%7C1574300971452%3B%20v8%3D1574299171470%7C1668907171470%3B%20v8_s%3DFirst%2520Visit%7C1574300971470%3B; s_sess=%20s_cpc%3D0%3B%20c21%3Dqs%253Doutcomes%2520of%2520split-thickness%2520skin%2520grafting%2520for%2520foot%2520and%2520ankle%2520wounds%2520in%2520patients%2520with%2520peripheral%2520arterial%2520disease.%2526authors%253Dcameron%2520m%2520akbari%3B%20e13%3Dqs%253Doutcomes%2520of%2520split-thickness%2520skin%2520grafting%2520for%2520foot%2520and%2520ankle%2520wounds%2520in%2520patients%2520with%2520peripheral%2520arterial%2520disease.%2526authors%253Dcameron%2520m%2520akbari%253A1%3B%20c13%3Drelevance-desc%3B%20e78%3Dqs%253DOutcomes%2520of%2520Split-thickness%2520Skin%2520Grafting%2520for%2520Foot%2520and%2520Ankle%2520Wounds%2520in%2520Patients%2520With%2520Peripheral%2520Arterial%2520Disease.%2526authors%253DCameron%2520M%2520Akbari%3B%20s_ppvl%3Dsd%25253Asearch%25253Aresults%25253Aarticles%252C100%252C16%252C4013%252C1536%252C722%252C1536%252C864%252C1.25%252CP%3B%20e41%3D1%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dsd%25253Aproduct%25253Ajournal%25253Aarticle%252C36%252C36%252C722%252C498%252C722%252C1536%252C864%252C1.25%252CL%3B; RT="z=1&dm=sciencedirect.com&si=ed735be7-6e47-4c44-98ef-a16eb1f71516&ss=k380x0h0&sl=5&tt=39u&bcn=%2F%2F173c5b09.akstat.io%2F&ld=5uo3&ul=5zgg',
    'referer': 'https://www.sciencedirect.com/search/advanced?qs=Outcomes%20of%20Split-thickness%20Skin%20Grafting%20for%20Foot%20and%20Ankle%20Wounds%20in%20Patients%20With%20Peripheral%20Arterial%20Disease.&authors=Cameron%20M%20Akbari&show=100',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
}

session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)
url = 'https://www.vitals.com/doctors/1nzc9k/elisabeth-kramer'
# page = requests.get(url,headers=header)
page = sess.get(url)
# print(page)
# print(page.text)
soup = bs4.BeautifulSoup(page.text, "lxml")
uni_grad = [(None, None)] * 3

# print(b.select('div[class="education"]'))

if soup.select('div[class="education"]'):
    div = 'div[class="education"]'
    span = 'span[class="location"]'
    p = 'p[class="education-text"]'
elif soup.select('div[class="card education"]'):
    div = 'div[class="card education"]'
    span = 'ul > li > span'
    p = 'ul > li > p'
# else:
#     return uni_grad
select_uni = div + ' > ' + span
select_grad = div + ' > ' + p

length = min(len(soup.select(select_uni)),
             len(soup.select(select_grad)))

for loop in range(length):
    university = soup.select(select_uni)[loop].text.strip()
    grad_year = soup.select(select_grad)[loop].text.strip()

    uni_grad[loop] = (university, grad_year)
print(uni_grad[0][0], uni_grad[0][1], uni_grad[1][0], uni_grad[1][1], uni_grad[2][0], uni_grad[2][0])
# print(b.select('div[class="education"] > span[class="location"]'))
# print(b.select('div[class="education"] > p[class="education-text"]'))

# data = {'size':5,'query_request':'Billings, Montana'}
# url_for_post = 'https://www.vitals.com/search/ajax_location?'
# page = sess.post(url_for_post,data=data)
# print(page.text)
# import pprint
#
# for doc in page.json()['hits']['hits']:
#     # doc_info = doc['_source']
#     pprint.pprint(
#         doc
#     )
