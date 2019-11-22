#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/10 21:12 
# @Author : Patrick 
# @File : dbConnectionCheck.py
# @Software: PyCharm

# Redis
# import redis
#
# client = redis.Redis(host='localhost', port=6379, decode_responses=True)
# for doc in client.keys('*'):
#     client.delete(doc)


# MySQL
import pymysql

#  local DB
# db = pymysql.connect(host="localhost", user='root', password='123456', database='DOCTORS')
# cursor = db.cursor()
# sql = """CREATE TABLE doctors (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,
#          SEX CHAR(1),
#          INCOME FLOAT )"""
# cursor.execute(sql)
# data = cursor.fetchone()
# print(data)
# db.close()


# AWS DB
mydb = pymysql.connect(
)
cursor = mydb.cursor()
sql = """
SELECT * FROM doctors_info.doctor;
"""
cursor.execute(sql)
l = cursor.fetchall()
for i in l:
    print(i)


# create table doctors
# (
#     VPID              VARCHAR(10)  NOT NULL UNIQUE,
#     NAME              VARCHAR(100) NOT NULL,
#     DEGREE            VARCHAR(100),
#     UNIVERSITY        VARCHAR(100),
# #     DEGREES           VARCHAR(100),
#     DISPLAY_TYPE      VARCHAR(100),
#     TYPE              VARCHAR(100),
#     SPECIALTIES       VARCHAR(500),
#     CITY              VARCHAR(100),
#     STATE             VARCHAR(100),
#     ADDRESS           VARCHAR(100),
#     LATITUDE          FLOAT,
#     LONGITUDE         FLOAT,
#     YEAR_EXP          FLOAT,
#     NUMBER_OF_RATINGS FLOAT,
#     OVERALL_RATINGS   FLOAT,
#     COMPANY           VARCHAR(100),
#     URL               VARCHAR(500),
#     CAMPAIGNS         VARCHAR(500),
#
#     PRIMARY KEY ('VPID')
# );
