#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/11 17:52 
# @Author : Patrick 
# @File : sessionCheck.py
# @Software: PyCharm

import cfscrape
import requests
import bs4
from src.Utilities.INFO import HEADER_VITALS

HEADER = HEADER_VITALS
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
