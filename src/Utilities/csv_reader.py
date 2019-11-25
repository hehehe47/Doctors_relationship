#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/11/25 15:00 
# @Author : Patrick 
# @File : csv_reader.py 
# @Software: PyCharm


import csv
import src.Utilities.DB_connector as conn

connector = conn.Connector('AWS')
cursor = connector.getCursor()

with open(r'E:\Python\Doctors_relationship\data\REAL\data.csv', encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        tmp = [i.strip() if i.strip() else None for i in row]
        tmp = [i if i and i[-1] != ',' else i[:-1] if i else None for i in tmp]

        firstname, lastname = tmp[0].split('_')
        firstname = firstname.replace('-', ' ')
        lastname = lastname.replace('-', ' ')
        li = [firstname, lastname]
        li += tmp[1:]
        sql = '''
        INSERT INTO real_doctor (first_name, last_name, department, company, city, country, email) 
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        '''
        print(sql % tuple(li))
        cursor.execute(sql, tuple(li))
    connector.commit()
    connector.close()
