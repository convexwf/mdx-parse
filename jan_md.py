# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : jan_md
# @FileName : jan_md.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-05-19 22:08
# @UpdateTime : Todo

from read_mdx import *

seqnum_list = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧']

def get_jan_md(queryWordList):
    md_info = [
        '# grammar',
        '',
    ]
    for queryWord in queryWordList:
        query_res = biaoxianwenxing_GetVocab(queryWord=queryWord, query_res={})
        md_info += [
            f"## {queryWord}",
            '',
            f'- **接续** {query_res["connect"]}',
            f'- **意思** {query_res["chinese_meaning"]}',
            f'- **注意** {query_res["explanation"]}',
            '',
            '- **例句**',
            '',
            '\n    '.join(['    ```jan'] + query_res["example"] + ['```']),
            '',
        ]
    with open('japanese.md', 'w+', encoding='utf-8') as fp:
        fp.write('\n'.join(md_info))

if __name__ == '__main__':
    get_jan_md([
        'あいだ',
        'あいだに',
    ])