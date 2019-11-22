#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/20 16:15 
# @Author : Patrick 
# @File : Create_sql_insert.py 
# @Software: PyCharm

import mysql.connector

client = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123456",
    database="doctors"
)
mycursor = client.cursor()

sql = '''
CREATE DATABASE IF NOT EXISTS DOCTORS;
USE DOCTORS;

CREATE TABLE IF NOT EXISTS DOCTOR
(
    VPID              VARCHAR(10)  NOT NULL,
    NAME              VARCHAR(100) NOT NULL,
    DEGREE            VARCHAR(100),
    UNIVERSITY        VARCHAR(100),
    GRAD_YEAR         VARCHAR(100),
    DISPLAY_TYPE      VARCHAR(100),
    TYPE              VARCHAR(100),
    SPECIALTIES       VARCHAR(500),
    CITY              VARCHAR(100),
    STATE             VARCHAR(100),
    ADDRESS           VARCHAR(100),
    LATITUDE          FLOAT,
    LONGITUDE         FLOAT,
    YEAR_EXP          FLOAT,
    NUMBER_OF_RATINGS FLOAT,
    OVERALL_RATINGS   FLOAT,
    COMPANY           VARCHAR(100),
    URL               VARCHAR(500),
    CAMPAIGNS         VARCHAR(500),
    OTHERS            VARCHAR(5000),
    PRIMARY KEY (VPID, NAME)
);

'''

mycursor.execute('select * from doctor where CAMPAIGNS is not null')
l = mycursor.fetchall()
for i in l:
    s = 'INSERT IGNORE INTO doctors.doctor (VPID, NAME, DEGREE, UNIVERSITY, GRAD_YEAR, DISPLAY_TYPE, TYPE, SPECIALTIES,' \
        'CITY, STATE, ADDRESS, LATITUDE, LONGITUDE, YEAR_EXP, NUMBER_OF_RATINGS, OVERALL_RATINGS, COMPANY, URL, ' \
        'CAMPAIGNS, OTHERS) VALUES ' + str(i)
    print(s)
