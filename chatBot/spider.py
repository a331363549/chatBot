from lxml import etree

from xlrd import open_workbook
from xlutils.copy import copy
import requests
import random
import re

headers = {
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 '}

url = 'https://m.chazidian.com/caipu/xiangcai/?&page='

req_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}

idx = 0


def get_page(index=1):
    URL = url + str(index)
    response = requests.get(URL, headers=req_headers)
    if response.status_code == 200:
        return response.text


def get_dish_name(text):
    selector = etree.HTML(text)
    dish_list = selector.xpath(r'//html/body/div[5]/div/p[1]/a[2]/text()')
    save_dish(dish_list)
    # with open('./dish.txt', 'a+', encoding='utf-8') as fw:
    #     for name in dish_list:
    #         fw.write(name + " nz\n")


def save_dish(dish_list):
    global idx
    for dish in dish_list:
        idx += 1
        ws.write(idx, 0, dish)
        ws.write(idx, 1, random.randrange(1, 3))
        ws.write(idx, 2, "我是" + dish)
        ws.write(idx, 3, random.randint(10, 50))
        ws.write(idx, 4, random.randrange(7, 10))
        wb.save('./dish.xlsx')
        print('saved第{}条数据'.format(idx))
    if idx < 50:
        get_dish_name(get_page(idx))


rb = open_workbook('./dish.xlsx')
rs = rb.sheet_by_index(0)
wb = copy(rb)
ws = wb.get_sheet(0)
get_dish_name(get_page())
