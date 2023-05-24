# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : jan_md
# @FileName : jan_md.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-05-19 22:08
# @UpdateTime : Todo

from read_mdx import *
from izaodao import *

md_header = [
    '# grammar',
    '',
]
number_list = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧']

def full_name(queryWord):
    with open(zaodao_url_file, 'r', encoding='utf-8') as fp:
        url_info = fp.readlines()
    
    for url_line in url_info:
        fullname = url_line.split('\t')[0]
        if queryWord in fullname:
            return fullname
    return queryWord

def translate_example(example):
    with open(zao_example_compress_file, 'r', encoding='utf-8') as fp:
        example_info = fp.readlines()
    for example_line in example_info:
        if example_line.startswith(example):
            return example_line.strip()
    return example

def get_jan_md(queryResList):
    md_info = []
    for query_res in queryResList:
        query_res['example'] = [translate_example(example) for example in query_res['example']]
        queryWord = full_name(query_res["queryWord"])
        connect = '\n'.join(query_res["connect"])
        chinese_meaning = '\n'.join(query_res["chinese_meaning"])
        md_info += [
            f"## {queryWord}",
            '',
            f'- **接续** {connect}',
            f'- **意思** {chinese_meaning}',
            f'- **注意**',
            '\n'.join([f'{number_list[i]} {explain}' for i, explain in enumerate(query_res["explanation"])]),
            '',
            '- **例句**',
            '',
            '\n    '.join(['    ```jan'] + query_res["example"] + ['```']),
            '',
        ]
    return md_info

if __name__ == '__main__':
    
    md_info = md_header
    
    # 从mdx文件中获取单词
    mdx_list = []
    # 从 zaodao 官网获取单词
    zaodao_list = []
    
    with open('data/203_grammar.txt', 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
        for line in lines:
            params = line.strip().split(' ')
            if params[0] == 'mdx':
                mdx_list.append(params[1])
            elif params[0] == 'zaodao':
                zaodao_list.append(params[1])
    
    mdx_queryResList = []
    for queryWord in mdx_list:
        query_res = biaoxianwenxing_GetVocab(queryWord=queryWord, query_res={})
        mdx_queryResList.append(query_res)
        # print(query_res)
    md_info += get_jan_md(mdx_queryResList)
    
    zaodao_queryResList = []
    for queryWord in zaodao_list:
        query_res = request_grammar(queryWord=queryWord, query_res={})
        zaodao_queryResList.append(query_res)
    
    with open('japanese.md', 'w+', encoding='utf-8') as fp:
        fp.write('\n'.join(md_info))