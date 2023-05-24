# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : izaodao
# @FileName : izaodao.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-05-21 12:55
# @UpdateTime : Todo

import requests
import sys
import io
import re
import time
import random
import hashlib
from lxml import etree
from collections import defaultdict, OrderedDict
from pyquery import PyQuery as pq    # pip install pyquery

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8') #改变标准输出的默认编码

base_url = 'http://grammar.izaodao.com/'

zaodao_url_file = 'data/grammar_url.txt'
zaodao_example_file = 'data/grammar_example.txt'
zao_example_compress_file = 'data/grammar_example_compress.txt'
zaodao_difference_file = 'data/grammar_difference.md'

def collect_url():
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    }
    
    grammar_info = []
    for NLevel in range(1, 6):
        entry_url = base_url + f'grammar.php?action=list&op=ajaxMoreList&level={NLevel}&cat=&cha='
        
        page = 0
        while True:
            page += 1
            print(f'Collecting {NLevel} level, page {page}...')
            page_response = requests.post(entry_url, headers=headers, data={'page': page})
            
            page_html = etree.HTML(page_response.text)
            page_result = page_html.xpath('//div[@class="list"]')
            page_text   = page_html.xpath('//div[@class="list"]/a')
            
            for td, text in zip(page_result, page_text):
                grammar_url = td.attrib.get('onclick').split("'")[1].replace('\n', '').strip()
                grammar_text = text.xpath('string(.)').replace('\n', '').strip()
                grammar_info.append('{}\t{}\n'.format(grammar_text, grammar_url))
                
            pattern = re.compile(r'后面还有(\d+)个语法')
            search_results = re.search(pattern, page_response.text)
            if len(search_results.groups()) == 0:
                print(f'Error: {page_response.text}')
                break
            if search_results.group(1) == '0':
                break
    
    with open(zaodao_url_file, 'w+', encoding='utf-8') as fp:
        fp.writelines(grammar_info)

def collect_examples():
    
    with open(zaodao_url_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()

    grammar_info = []   
    for idx, line in enumerate(lines):
        print(f'Collecting {idx}...line: {line.strip()}')
        sys.stdout.flush()
        params = line.strip().split('\t')
        if len(params) < 2:
            print('Error: {}'.format(line))
            break
        grammar_text = params[0]
        grammar_url = base_url + params[1]
        
        ## random sleep (0.1s ~ 1s)
        try:
            sleepTime = random.randint(1, 10) / 10
            for _ in range(5):
                time.sleep(sleepTime)
                response = requests.get(grammar_url, timeout=5)
                if response.status_code == 200:
                    break
                sleepTime *= 2
        except Exception:
            print('Error: id: {}, url: {}'.format(idx, grammar_url))
            continue

        grammar_html = etree.HTML(response.text)
        
        # with open('result/z.html', 'w+', encoding='utf-8') as fp:
        #     fp.write(response.text)
        
        # 从html中提取需要的部分。
        doc = pq(grammar_html)
        
        titleBlock = list(doc('div[@class="box1"] > span').items())
        if len(titleBlock) > 0:
            title = titleBlock[0].text().replace('\n', '').strip()

        grammar_info.append('{}\t{}\t{}\n'.format(grammar_text, title, grammar_url))
        
        exampleBlock = list(doc('dl > dd > ul > li').items())
        for example in exampleBlock:
            example = example.text()[1:].replace('\n', '').strip()
            grammar_info.append('△ {}\n'.format(example))
            # print("example: {}".format(example))
        print('example-length: {}'.format(len(exampleBlock)))
    
    with open(zaodao_example_file, 'w+', encoding='utf-8') as fp:
        fp.writelines(grammar_info)

def compress_examples():
    with open(zaodao_example_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    zaodao_example_set = OrderedDict()
    for line in lines:
        if line.startswith('△ '):
            zaodao_example_set[line] = 1
    with open(zao_example_compress_file, 'w+', encoding='utf-8') as fp:
        fp.writelines(zaodao_example_set.keys())

def collect_difference():
    with open(zaodao_url_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    number_list = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧', '⑨']
    grammar_info = ['# 易混淆语法辨析\n\n']
    grammer_dict = defaultdict(int)
    for idx, line in enumerate(lines):
        sys.stdout.flush()
        params = line.strip().split('\t')
        if len(params) < 2:
            print('Error: {}'.format(line))
            break
        grammar_text = params[0]
        grammar_url = base_url + params[1]
        print(f'Collecting {idx}...line: {grammar_text}')
        
        ## random sleep (0.1s ~ 1s)
        try:
            sleepTime = random.randint(1, 10) / 10
            for _ in range(5):
                time.sleep(sleepTime)
                response = requests.get(grammar_url, timeout=5)
                if response.status_code == 200:
                    break
                sleepTime *= 2
        except Exception:
            print('Error: id: {}, url: {}'.format(idx, grammar_url))
            continue
        
        grammar_html = etree.HTML(response.text)
        
        doc = pq(grammar_html)
        
        differenceBlock = list(doc('dt:contains("易混淆语法辨析") + dd').items())
        
        if len(differenceBlock) == 0:
            continue
        
        differenceBlock = differenceBlock[0]
        # 替换多个换行符为一个
        difference = re.sub(r'\n+', '\n', differenceBlock.text().replace(' ', '').strip())
        # print(difference)
        
        difference_title = difference.split('\n')[0]
        grammer_dict[difference_title] += 1
        if grammer_dict[difference_title] > 1:
            print(f"{difference_title} has been collected.")
            continue
        
        
        analysis_flag = True
        difference_analysis, difference_example = [], []
        for line in difference.split('\n')[2:]:
            line = line.strip()
            if '【例句】' in line:
                analysis_flag = False
                continue
            if analysis_flag:
                if line[0] in number_list:
                    difference_analysis.append(line[1:].strip())
                elif len(difference_analysis) == 0:
                    difference_analysis.append(line.strip())
                else:
                    difference_analysis[-1] += ("," + line.strip())
            else:
                difference_example.append('△ ' + line.strip()[1:])
        
        grammar_info += [
            f"## 【{difference_title}】\n",
            "\n",
            "### 解析\n",
            "\n",
            '\n'.join([f'- {it}' for it in difference_analysis]),
            "\n\n",
            "```jan\n",
            '\n'.join([f'{it}' for it in difference_example]),
            "\n```\n"
            "\n"
            "### 原文\n",
            "\n",
            f"{difference}",
            "\n\n",
        ]
        
    with open(zaodao_difference_file, 'w+', encoding='utf-8') as fp:
        fp.writelines(grammar_info)

def request_grammar(queryWord, query_res):
    with open(zaodao_url_file, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    
    queryUrl = ''
    for idx, line in enumerate(lines):
        if queryWord in line:
            query_res['queryWord'] = line.strip().split('\t')[0]
            queryUrl = line.strip().split('\t')[1]
            break
    
    if len(queryUrl) == 0:
        print(f'Not found {queryWord}')
        return
    
    grammar_url = base_url + queryUrl
    ## random sleep (0.1s ~ 1s)
    try:
        sleepTime = random.randint(1, 10) / 10
        for _ in range(5):
            response = requests.get(grammar_url, timeout=5)
            if response.status_code == 200:
                break
            else:
                print('Error request : id: {}, url: {}, error: {}'.format(idx, grammar_url, response.text))
            time.sleep(sleepTime)
            sleepTime *= 2
    except Exception:
        print('Error request: id: {}, url: {}'.format(idx, grammar_url))
        return
    
    grammar_html = etree.HTML(response.text)
        
    doc = pq(grammar_html)
    
    # with open("result/zaodao.html", 'w+', encoding='utf-8') as fp:
    #     fp.write(doc.html())    
    
    query_res['title'] = []
    titleBlock = list(doc('div[@class="box1"]').items())
    for title in titleBlock:
        title = title.text().replace('\n', '').strip()
        query_res['title'].append(title)
        
    query_res['connect'] = []
    connectBlock = list(doc('div[class="box2"] > div[class="mark1"]').items())
    for connect in connectBlock:
        connect = connect.text()[2:].replace('\n', '').strip()
        query_res['connect'].append(connect)
        
    query_res['chinese_meaning'] = []
    meaningBlock = list(doc('div[class="mark2-1"]').items())
    for meaning in meaningBlock:
        if not meaning.text().startswith('意思'):
            continue
        meaning = meaning.text().split('\xa0')[-1].replace('\n', '').strip()
        query_res['chinese_meaning'].append(meaning)
        
    query_res['explanation'] = []
    explanationBlock = list(doc('div > dl > dt:contains("注意")').items())
    for explanation in explanationBlock:
        explanation = explanation.next()
        re.sub(r'\n+', '\n', explanation.text().replace(' ', '').strip())
        for line in explanation.text().split('\n'):
            line = line.strip()
            if len(line) > 0:
                query_res['explanation'].append(line[2:].strip())
        
        
    query_res['example'] = []
    exampleBlock = list(doc('dl > dd > ul > li').items())
    for example in exampleBlock:
        example = example.text().replace('\n', '')[1:].strip()
        query_res['example'].append('△ ' + example)
        
    return query_res
            
        

if __name__ == '__main__':
    collect_url()  
    # collect_examples()
    # compress_examples()
    # collect_difference()
    
    # print(request_grammar('からみると', {}))
    # print(request_grammar('いかにも', {}))