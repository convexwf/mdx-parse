# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : read_excel
# @FileName : read_excel.py
# @Author : convexwf@gmail.com
# @CreateDate : 2022-10-09 12:36
# @UpdateTime : Todo

import xlrd

filename = 'GRE红宝书正序+乱序.xlsx'
sheet_index = 0

def read_word():
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_index(sheet_index)
    results = []
    for row in range(1, table.nrows):
        item = table.row_values(row)
        if len(item[2]) > 0:
            # results.append([item[0], item[1]])
            results.append(item[0])
    return results

if __name__ == '__main__':
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_index(sheet_index)
    
    results = []
    for row in range(1, table.nrows):
        item = table.row_values(row)
        if len(item[2]) > 0:
            results.append([item[0], item[1], item[2], item[3]])
        if len(item[4]) > 0:
            results.append([item[0], item[1], item[4], item[5]])
        if len(item[6]) > 0:
            results.append([item[0], item[1], item[6], item[7]])
    
    to_write = ['|' + ' | '.join(it) + '|\n' for it in results]
    with open('out.md', 'w+', encoding='utf-8') as fp:
        fp.writelines(to_write)
    