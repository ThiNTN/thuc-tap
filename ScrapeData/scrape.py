#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests #lay html tu trang web
import bs4 #lay du lieu tu web
import numpy as np  #lam viec voi ma tran
import pandas as pd # xu ly du lieu va luu du lieu
import time


def get_html_resource(url):
    #lay source html cua trang web
    response = requests.get(url)
    html = response.content

    return bs4.BeautifulSoup(html, "html.parser")


def create_districts_dict(soup):
    #tao tu dien cac quan
    districts = {}
    selects = soup.findAll("select", {"id": "duan_huyen"})
    for select in selects:
        for option in select.find_all('option'):
            districts[option['value']] = option.text

    del districts['0']  #0 khong chon quan nao nen xoa(del)
    return districts #tra ve tu dien cac quan


file_path = 'my_excel_file.xlsx' #tenfile luu ve
url = 'https://cafeland.vn/bang-gia-du-an/0-63-147-2-nokey/'
soup = get_html_resource(url)
districts = create_districts_dict(soup)
print(districts)
writer = pd.ExcelWriter(file_path) #cong cu ho tro du lieu


for key, district in districts.items():
    #lay du lieu tung bang cua tung quan
    url = 'https://cafeland.vn/bang-gia-du-an/0-63-' + key + '-2-nokey/'
    list_of_rows = []
    soup = get_html_resource(url)
    tables = soup.findAll("table") #tim bang
    for table in tables:
        #Here you can do whatever you want with the data! You can findAll table row headers, etc...
        for row in table.findAll('tr'):
            list_of_cells = []
            for cell in row.findAll('td'):
                text = cell.text.replace('&nbsp;', '')
                text = text.replace('\n', '')
                text = text.replace('\t', '')
                text = " ".join(text.split())
                text = text.encode('utf8')
                list_of_cells.append(text)
            list_of_rows.append(list_of_cells)
    list_of_rows = np.asarray(list_of_rows) #chuyen ve thanh mang
    df = pd.DataFrame(list_of_rows[1:-1]) #chuyen ve thanh dataframe

    ## save to xlsx file
    df.to_excel(writer, district)
    time.sleep(10)
writer.save()
writer.close()
