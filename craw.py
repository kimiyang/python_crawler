#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import requests
from bs4 import BeautifulSoup
import codecs
import sys

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

def get_sgyuan_house_rent_info(url, encoding=None, exclude_keywords=[], within_days=5, min_money=600, max_money=1200):
    response = requests.get(url)
    if encoding:
        response.encoding = encoding
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    title = soup.find('title').string
    list  = soup.find_all('div', 'media-body')
    file = codecs.open('test.txt', 'a','utf-8')
    count = 0
    for l in list:
        href = ''
        name = 'no name'
        day = ''
        money = ''
        # print int(l.div.contents[2][0:2])

        if l.a['href']:
            href = l.a['href']
        if l.a.string:
            name = l.a.string
        if l.div.contents[2]:
            day = l.div.contents[2]
        if l.find('span', 'money'):
            money = l.find('span', 'money').string


        time_condition = u'天' not in day or int(l.div.contents[2][0:l.div.contents[2].index(u'天')]) < within_days

        keywords_condition = True
        for word in exclude_keywords:
            if word in name:
                keywords_condition = False
                break

        money_condition = True

        try:
            money_int = int(money[1:])
            if(money_int > max_money or money_int < min_money):
                money_condition = False
                print name + 'money not fit %d' % money_int
        except:
            print 'convert ' + money[1:] + ' error'

        if keywords_condition and time_condition and money_condition:
            output_str = '**'+name + '    ' + href + '    ' + day + '  ' + money +'**'
            print output_str
            count += 1
            file.write(output_str+'\n')



    file.close()
    print url + ' craw done... crawled: %d' % count
    return count


if __name__ == '__main__':
    # get_html('http://www.qq.com', 'gb2312')
    count = 0
    for x in range(1, 200):
        count += get_sgyuan_house_rent_info(url='http://www.sgyuan.com/category/view/id/15/area_id/'+str(x), exclude_keywords=[u'限女生', u'床位', u'短期', u'女孩'], within_days=5, min_money=600, max_money=1200)
    print 'Completed! Total crawled: %d' % count
