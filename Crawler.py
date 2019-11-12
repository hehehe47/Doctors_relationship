#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/10 14:07
# @Author : Patrick 
# @File : Crawler.py 
# @Software: PyCharm

import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint as pprint
import redis

SLEEP_TIME = 5
URL = 'https://www.vitals.com/search/ajax?display_type=Doctor&city_state=Washington,%20DC&latLng=38.892091,-77.024055&reqNo=0'
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
NUM = 10000


def build_connection():
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        client = redis.Redis(connection_pool=pool)
        client.ping()  # Test DB connection
    except redis.ConnectionError as err_conn:
        print("Connection Error: ", err_conn)
        exit(0)
    return client


def check_exists(doc_name):
    return True if doc_name in keys else False


def update_json(doc_info):
    """
        info for each doc
        {'city_state': 'Washington, DC',
         'degree': 'MD',
         'degrees': 'MD',
         'display_name': 'Dr. Gina OrTon',
         'display_type': 'Doctor',
         'locations': [{'_geoloc': {'lat': '38.89420000', 'lng': '-77.02460000'},
                        'address1': '935 Pennsylvania Ave NW',
                        'city': 'Washington',
                        'state': 'DC'}],
         'number_of_ratings': 1,
         'overall_rating': 5,
         'site': {'vitals': {'slug': 'Dr_Gina_Orton.html',
                             'url': '/doctors/Dr_Gina_Orton.html'}},
         'slug': 'Dr_Gina_Orton.html',
         'specialties': ['Psychiatry'],
         'type': 'doctor',
         'url': '/doctors/Dr_Gina_Orton.html',
         'vpid': 'zwkx5h'}
        """
    doc_info['address'] = doc_info['locations'][0]['address1']
    # pprint(doc_info['locations'])
    doc_info['lat'] = str(doc_info['locations'][0]['_geoloc']['lat'])
    doc_info['lng'] = str(doc_info['locations'][0]['_geoloc']['lng'])
    doc_info['url'] = 'https://www.vitals.com' + doc_info['url']
    for ke, ve in doc_info.items():
        if ve and type(ve) == list and ve != 'locations':
            doc_info[ke] = ve[0]
    need_to_pop = [k for k, v in doc_info.items() if type(v) == list or type(v) == dict]
    need_to_pop.append('display_name')
    for item in need_to_pop:
        doc_info.pop(item)


def save_docs(sess, url):
    try:
        page = sess.get(url)
        page.raise_for_status()
        page_json = page.json()
        doctors = page_json['hits']['hits']
        for doc in doctors:
            doc_info = doc['_source']
            doc_name = doc_info['display_name']
            if check_exists(doc_name):
                continue
            update_json(doc_info)
            try:
                # print(doc_name)
                client.hmset(name=doc_name, mapping=doc_info)
            except redis.exceptions.DataError as err_data:
                print(doc_info)
                print(err_data)
        # exit(0)

    except requests.exceptions.HTTPError as errh:
        print("Http Error: ", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting: ", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error: ", errt)
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else ", err)

    time.sleep(SLEEP_TIME)
    # pass


client = build_connection()

keys = set(client.keys('*'))

session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)

total_num = sess.get(URL).json()['hits']['total']  # get total number of doctors
count = 0
for i in range(total_num // 21):  # each page contains 21 doctors
    print('Page ' + str(i) + ' start!')
    save_docs(sess, URL + '&page=' + str(i))  # loop for those pages
    count += 1
    print('Page ' + str(i) + ' complete!')
    if count == NUM:
        print('Complete ' + str(NUM) + 'docs')
        exit(0)
