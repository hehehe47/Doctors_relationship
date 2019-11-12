#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/11 17:52 
# @Author : Patrick 
# @File : sessionCheck.py
# @Software: PyCharm

import cfscrape
import requests

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

session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)
url = 'https://www.vitals.com/search/ajax?display_type=Doctor&city_state=Washington,%20DC&latLng=38.892091,-77.024055&reqNo=0&page=476'
page = sess.get(url)
print(page)
print(page.text)
import pprint

pprint.pprint(page.json())
