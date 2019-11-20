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
import mysql.connector
import random

SLEEP_TIME = 10
URL = 'https://www.vitals.com/search/ajax?city_state=Washington,%20DC&latLng=38.892091,-77.024055&reqNo=0'
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
NOT_CRAWL = {'Hospital', 'Pharmacy', 'Urgent Care Center', 'Group Practice', 'Nursing Home', 'Cancer Center'}


def redis_build_connection():
    try:
        pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
        client = redis.Redis(connection_pool=pool)
        client.ping()  # Test DB connection
    except redis.ConnectionError as err_conn:
        print("Connection Error: ", err_conn)
        exit(0)
    return client


def mysql_build_connection():
    try:
        client = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="123456",
            database="doctors"
        )
    except mysql.connector.Error as err_conn:
        print("Connection Error: ", err_conn)
        exit(0)
    return client


# def check_exists(doc_name):
#     return True if doc_name in keys else False


# def update_json(doc_info):
#     """
#         info for each doc
#         {'city_state': 'Washington, DC',
#          'degree': 'MD',
#          'degrees': 'MD',
#          'display_name': 'Dr. Gina OrTon',
#          'display_type': 'Doctor',
#          'locations': [{'_geoloc': {'lat': '38.89420000', 'lng': '-77.02460000'},
#                         'address1': '935 Pennsylvania Ave NW',
#                         'city': 'Washington',
#                         'state': 'DC'}],
#          'number_of_ratings': 1,
#          'overall_rating': 5,
#          'site': {'vitals': {'slug': 'Dr_Gina_Orton.html',
#                              'url': '/doctors/Dr_Gina_Orton.html'}},
#          'slug': 'Dr_Gina_Orton.html',
#          'specialties': ['Psychiatry'],
#          'type': 'doctor',
#          'url': '/doctors/Dr_Gina_Orton.html',
#          'vpid': 'zwkx5h'}
#         """
#     doc_info['address'] = doc_info['locations'][0]['address1']
#     # pprint(doc_info['locations'])
#     doc_info['lat'] = str(doc_info['locations'][0]['_geoloc']['lat'])
#     doc_info['lng'] = str(doc_info['locations'][0]['_geoloc']['lng'])
#     doc_info['url'] = 'https://www.vitals.com' + doc_info['url']
#     for ke, ve in doc_info.items():
#         if ve and type(ve) == list and ve != 'locations':
#             doc_info[ke] = ve[0]
#     need_to_pop = [k for k, v in doc_info.items() if type(v) == list or type(v) == dict]
#     need_to_pop.append('display_name')
#     for item in need_to_pop:
#         doc_info.pop(item)

def get_detail(json, key):
    key = key.lower()
    if key == 'specialties':
        return json.get(key, [''])[0]
    elif key == 'city' or key == 'state' or key == 'address1':
        return json.get('locations')[0][key]
    elif key == 'lng' or key == 'lat':
        return json.get('locations')[0]['_geoloc'][key]
    elif key == 'url':
        return 'https://www.vitals.com' + json.get(key)
    elif key == 'campaigns':
        campaign = json.get(key, None)
        if campaign:
            return campaign[0]['campaign_name']
    else:
        return json.get(key, None)


def get_doc_university(url):
    grad_year, university = '', ''
    req = sess.get(url)
    soup = bs(req.text, features="lxml")
    try:
        university = soup.select('div[class="card education"] > ul > li > span')[
            0].text.strip()  # soup.select('div > span')
        grad_year = soup.select('div[class="card education"] > ul > li > p')[
            0].text.strip()  # soup.select('div > span')
    except IndexError:
        pass
    try:
        university = soup.select('div[class="education"] > span')[0].text.strip()  # soup.select('div > span')
        grad_year = soup.select('div[class="education"] > p')[0].text.strip()  # soup.select('div > span')
    except IndexError:
        pass
    if len(grad_year) > 4 and grad_year[-4:].isnumeric():
        grad_year = grad_year[-4:]
    elif len(grad_year) < 4 or grad_year != 'Residency':
        grad_year = ''
    return university, grad_year


def save_docs(sess, url):
    try:
        page = sess.get(url)
        page.raise_for_status()
        page_json = page.json()
        doctors = page_json['hits']['hits']
        for doc in doctors:
            doc_info = doc['_source']
            dis_type = get_detail(doc_info, 'DISPLAY_TYPE')
            if dis_type in NOT_CRAWL:
                continue
            doc_name = doc_info['display_name']
            doc_url = get_detail(doc_info, 'URL')
            university, grad_year = get_doc_university(doc_url)

            # if check_exists(doc_name):
            #     continue
            # update_json(doc_info)
            try:
                sql = "INSERT INTO doctor (VPID,NAME,DEGREE,UNIVERSITY,GRAD_YEAR,DISPLAY_TYPE,TYPE,SPECIALTIES,CITY," \
                      "STATE,ADDRESS,LATITUDE,LONGITUDE,YEAR_EXP,NUMBER_OF_RATINGS,OVERALL_RATINGS,COMPANY,URL," \
                      "CAMPAIGNS,OTHERS) " \
                      "VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                val = (
                    get_detail(doc_info, 'vpid'), doc_name, get_detail(doc_info, 'degree'),
                    university, grad_year,
                    get_detail(doc_info, 'DISPLAY_TYPE'), get_detail(doc_info, 'TYPE'),
                    get_detail(doc_info, 'SPECIALTIES'),
                    get_detail(doc_info, 'CITY'), get_detail(doc_info, 'STATE'), get_detail(doc_info, 'ADDRESS1'),
                    get_detail(doc_info, 'lat'), get_detail(doc_info, 'lng'), get_detail(doc_info, 'years_experience'),
                    get_detail(doc_info, 'NUMBER_OF_RATINGS'), get_detail(doc_info, 'overall_rating'),
                    get_detail(doc_info, 'company_name'),
                    get_detail(doc_info, 'URL'), get_detail(doc_info, 'CAMPAIGNS'), get_detail(doc_info, 'OTHERS'))
                cursor.execute(sql, val)
                client.commit()
                # exit(0)
            except mysql.connector.Error as err:
                # print(doc_name)
                print(err)
        # exit(0)

    except requests.exceptions.HTTPError as errh:
        print("Http Error: ", errh)
        return False
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting: ", errc)
        return False
    except requests.exceptions.Timeout as errt:
        print("Timeout Error: ", errt)
        return False
    except requests.exceptions.RequestException as err:
        print("OOps: Something Else ", err)
        return False

    time.sleep(random.randint(1, SLEEP_TIME))
    return True
    # pass


client = mysql_build_connection()
cursor = client.cursor()

session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)

total_num = sess.get(URL).json()['hits']['total']  # get total number of doctors
print(total_num)
# exit(0)
count = 0
for i in range(305, total_num // 21):  # each page contains 21 doctors   # 256
    # for i in range(10):  # each page contains 21 doctors
    print('Page ' + str(i) + ' start!')

    if not save_docs(sess, URL + '&page=' + str(i)):  # loop for those pages
        print('Stop due to http error')
        print('Current number: ' + str(count))
        exit(0)
    count += 1
    print('Page ' + str(i) + ' complete!')
    if count == total_num:
        print('Complete ' + str(NUM) + 'docs')
        exit(0)
