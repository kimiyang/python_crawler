#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import codecs

def get_html(url, encoding=None):
    response = requests.get(url)
    if encoding:
        response.encoding = encoding
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # cust
    list = soup.find_all('h3')
    file = codecs.open('test.txt', 'w','utf-8')
    for l in list:
        file.write(l.a.string+'    '+l.a.get('href')+'\n')
    file.close()
    print 'craw done...'

if __name__ == '__main__':
    get_html('http://www.qq.com', 'gb2312')
