#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/26 17:15 
# @Author : Patrick 
# @File : demo.py
# @Software: PyCharm


# https://www.mendeley.com/profiles/7006699573/preview/?sd=1&border=0 小窗


import cfscrape
import requests
import bs4
import json
import pprint
from src.Utilities.INFO import HEADER_DEMO

HEADER = HEADER_DEMO

AUTHOR = 'Geoffrey%20Hinton'


def traverse_authors(pii, doi):
    '''
    只有pii以S开头的作者才会有对应的小弹窗
     'authors': [{'name': 'Ruslan Salakhutdinov', 'order': 0},
                 {'name': '<em>Geoffrey</em> <em>Hinton</em>', 'order': 1}],    
    '''
    doi = doi.replace('/', '%2F')
    co_auth_link = 'https://api.plu.mx/widget/elsevier/artifact?type=doi&id=' + doi + \
                   '&hidePrint=true&onSuccess=onMetricsWidgetSuccess&passHiddenCategories=true&site=plum&href' \
                   '=https%3A%2F%2Fplu.mx%2Fplum%2Fa%2F%3Fdoi%3D' \
                   + doi + '&isElsWidget=true&theme=plum-sciencedirect-theme '
    req = requests.get(co_auth_link).json()
    auth_list = req['authors']
    auth_id = [None for _ in range(len(auth_list))]
    if pii.startswith('S'):
        auth_id = []
        for num in range(len(auth_list)):
            auth_link = 'https://www.sciencedirect.com/sdfe/arp/pii/' + pii + '/author/' + str(num + 1) + '/articles'
            req = sess.get(auth_link)
            try:
                auth_id.append(req.json()['scopusAuthorId'])
            except Exception as e:
                print('Error happened at get author_id: ', e)
    print(list(zip(auth_list, auth_id)))


session = requests.Session()
session.headers = HEADER
sess = cfscrape.create_scraper(sess=session)

# 按名字搜索论文 显示100个 没找到论文100个以上的作者还不知道第101篇怎么遍历哈哈哈哈
url = 'https://www.sciencedirect.com/search/api?authors=' + AUTHOR + '&show=100&navigation=true'

page = sess.get(url)
# print(page.text)
# soup = bs4.BeautifulSoup(page.text, features='lxml')
#
# # 所有论文条目在 最下面的script标签中的一个 json是以‘var INITIAL_STATE = ’开始的
# phrase_json = soup.select('script[type]')[7].text[len('var INITIAL_STATE = '):]
# paper_json = json.loads(phrase_json)
# import pprint
#
# pprint.pprint(paper_json)
#
# # 包含每篇论文所有信息的list
# paper_list = paper_json['search']['searchResults']
# print(len(paper_list))

# 每篇论文带详细信息的json 可以研究一哈，里面有按年统计之类的各种统计数据
page_json = page.json()
how_many_paper = page_json['resultsFound']
paper_list = page_json['searchResults']

for paper in paper_list[:]:
    '''
    'abstTypes': ['author'],
     'articleType': 'FLA',
     'articleTypeDisplayName': 'Research article',
     'authors': [{'name': 'Ruslan Salakhutdinov', 'order': 0},
                 {'name': '<em>Geoffrey</em> <em>Hinton</em>', 'order': 1}],
     'cid': 271876,
     'contentType': 'JL',
     'documentSubType': 'fla',
     'doi': '10.1016/j.ijar.2008.11.006',
     'issn': '0888613X',
     'itemStage': 'S300',
     'link': '/science/article/pii/S0888613X08001813',
     'openAccess': True,
     'openArchive': True,
     'pages': {'first': '969', 'last': '978'},
     'pdf': {'downloadLink': '/science/article/pii/S0888613X08001813/pdfft?md5=8fe2f3860bf58ac305fd5e76e6088b74&pid=1-s2.0-S0888613X08001813-main.pdf',
             'filename': '1-s2.0-S0888613X08001813-main.pdf',
             'getAccessLink': '/science/article/pii/S0888613X08001813'},
     'pii': 'S0888613X08001813',
     'publicationDate': '2009-07-31',
     'publicationDateDisplay': 'July 2009',
     'sortDate': '2009-07-01T00:00:00.000Z',
     'sourceTitle': 'International Journal of Approximate Reasoning',
     'sourceTitleUrl': '/science/journal/0888613X',
     'title': 'Semantic hashing',
     'volumeIssue': 'Volume 50, Issue 7'}
    '''
    paper_link = paper['link']
    pii = paper['pii']
    # 该篇文章部分作者
    # 会有下面这种情况
    '''
    'authors': [{'name': 'Andrew Miles', 'order': 0},
                {'name': 'Colin Graham', 'order': 1},
                {'name': 'Chris Hawkesworth', 'order': 2},
                {'name': 'Martin Gillespie', 'order': 3},
                {'name': 'EMMAC', 'order': 6}]
    '''
    authors = paper['authors']
    doi = paper['doi']
    # 最后一个作者的order作为总个数
    num_of_authors = authors[-1]['order']
    print(paper['title'])
    traverse_authors(pii, doi)
    print('---------------------------')
