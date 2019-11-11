#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/10 21:12 
# @Author : Patrick 
# @File : Connection.py 
# @Software: PyCharm

import redis

client = redis.Redis(host='localhost', port=6379, decode_responses=True)
for doc in client.keys('*'):
    client.delete(doc)
