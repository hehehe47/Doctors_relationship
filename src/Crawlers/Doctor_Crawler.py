#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/10 14:07
# @Author : Patrick 
# @File : Doctor_Crawler.py
# @Software: PyCharm

import requests
import cfscrape
from bs4 import BeautifulSoup as bs
import time
from pprint import pprint as pprint
import redis
import mysql.connector
import random
import src.Utilities.DB_connector as connector
from src.Utilities.INFO import HEADER_VITALS

SLEEP_TIME = 10
URL = 'https://www.vitals.com/search/ajax?city_state=Washington,%20DC&latLng=38.892091,-77.024055&reqNo=1'
HEADER = HEADER_VITALS
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
        specialties = json.get(key, None)
        if specialties:
            return ','.join(specialties)
        # return json.get(key, [''])[0]
    elif key == 'city' or key == 'state' or key == 'address1':
        return json.get('locations')[0][key]
    elif key == 'lng' or key == 'lat':
        return json.get('locations')[0]['_geoloc'][key]
    elif key == 'url':
        return 'https://www.vitals.com' + json.get(key)
    elif key == 'degree':
        degree = json.get(key)
        return degree if degree else None
    elif key == 'campaigns':
        campaign = json.get(key, None)
        if campaign:
            return campaign[0]['campaign_name']
    else:
        return json.get(key, None)


def vaild_uni_grad(university, grad_year):
    if grad_year and len(grad_year) > 4 and grad_year[-4:].isnumeric():
        grad_year = grad_year[-4:]
    elif not grad_year or len(grad_year) < 4 or grad_year != 'Residency':
        grad_year = None
    if not university or len(university) < 2:
        grad_year = None
        university = None
    return university, grad_year


def get_doc_university(url):
    req = sess.get(url)
    soup = bs(req.text, features="lxml")
    uni_grad = [(None, None)] * 2

    if soup.select('div[class="education"]'):
        div = 'div[class="education"]'
        span = 'span[class="location"]'
        p = 'p[class="education-text"]'
    elif soup.select('div[class="card education"]'):
        div = 'div[class="card education"]'
        span = 'ul > li > span'
        p = 'ul > li > p'
    else:
        return uni_grad
    select_uni = div + ' > ' + span
    select_grad = div + ' > ' + p

    length = min(len(soup.select(select_uni)),
                 len(soup.select(select_grad)),
                 2)

    for loop in range(length):
        university = soup.select(select_uni)[loop].text.strip()
        grad_year = soup.select(select_grad)[loop].text.strip()

        uni_grad[loop] = vaild_uni_grad(university, grad_year)


    return uni_grad


def format_name(doc_name):
    if doc_name.startswith('Dr.'):
        doc_name = doc_name.lstrip('Dr.').lstrip()
    return doc_name


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
            doc_name = format_name(doc_info['display_name'])
            doc_url = get_detail(doc_info, 'URL')
            uni_grad = get_doc_university(doc_url)

            # if check_exists(doc_name):
            #     continue
            # update_json(doc_info)
            try:
                sql = "INSERT INTO doctor (VPID,NAME,DEGREE,UNIVERSITY1,GRAD_YEAR1,UNIVERSITY2,GRAD_YEAR2," \
                      "DISPLAY_TYPE,TYPE,SPECIALTIES,CITY,STATE,ADDRESS,LATITUDE,LONGITUDE," \
                      "YEAR_EXP,NUMBER_OF_RATINGS,OVERALL_RATINGS,COMPANY,URL,CAMPAIGNS,OTHERS) VALUES (%s, %s, %s, " \
                      "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "
                val = (
                    get_detail(doc_info, 'vpid'), doc_name, get_detail(doc_info, 'degree'),
                    uni_grad[0][0], uni_grad[0][1], uni_grad[1][0], uni_grad[1][1],
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


client = connector.Connector('AWS')
cursor = client.getCursor()

session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)

total_num = sess.get(URL).json()['hits']['total']  # get total number of doctors
print(total_num)
# exit(0)
count = 0
# for i in range():  # each page contains 21 doctors   # 476
for i in range(399, total_num // 21):  # each page contains 21 doctors   # 476
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
