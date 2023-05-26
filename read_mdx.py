# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : read_mdx
# @FileName : read_mdx.py
# @Author : convexwf@gmail.com
# @CreateDate : 2022-10-19 19:31
# @UpdateTime : Todo

import os
from readmdict import MDX, MDD  # pip install readmdict
from pyquery import PyQuery as pq    # pip install pyquery

'''
# 如果是windows环境，运行提示安装python-lzo，但
> pip install python-lzo
报错“please set LZO_DIR to where the lzo source lives” ，则直接从 https://www.lfd.uci.edu/~gohlke/pythonlibs/#_python-lzo 下载 "python_lzo‑1.12‑你的python版本.whl" 
> pip install xxx.whl 
装上就行了，免去编译的麻烦
'''

collins_flag = False
oxford_flag = False
thelittle_flag = False
biaoxianwenxing_flag = True

if collins_flag:
    collins_filename  = "CollinsCOBUILDOverhaul V 2-30.mdx"
    collins_headwords = [*MDX(collins_filename)]            # 单词名列表
    collins_items     = [*MDX(collins_filename).items()]    # 释义html源码列表

if oxford_flag:
    oxford_filename  = "牛津高阶(第10版 英汉双解)V13_2.mdx"
    oxford_headwords = [*MDX(oxford_filename)]            # 单词名列表
    oxford_items     = [*MDX(oxford_filename).items()]    # 释义html源码列表

if thelittle_flag:
    thelittle_filename  = 'TheLittle.mdx'
    thelittle_headwords = [*MDX(thelittle_filename)]            # 单词名列表
    thelittle_items     = [*MDX(thelittle_filename).items()]    # 释义html源码列表

if biaoxianwenxing_flag:
    biaoxianwenxing_filename  = "dict/日本語表現文型辞典_20190729/日本語表現文型辞典.mdx"
    biaoxianwenxing_headwords = [*MDX(biaoxianwenxing_filename)]            # 单词名列表
    biaoxianwenxing_items     = [*MDX(biaoxianwenxing_filename).items()]    # 释义html源码列表
    with open('result/index.md', 'w+', encoding='utf-8') as fp:
        fp.write('\n'.join([it.decode() for it in biaoxianwenxing_headwords]))

def init():
    if collins_flag and len(collins_headwords) != len(collins_items):
        print(f'【ERROR】柯林斯高阶双解辞典 加载失败{len(collins_headwords)}, {len(collins_items)}')
        os._exit(-1)
    if oxford_flag and len(oxford_headwords) != len(oxford_items):
        print(f'【ERROR】牛津高阶辞典 加载失败{len(oxford_headwords)}, {len(oxford_items)}')
        os._exit(-1)
    if thelittle_flag and len(thelittle_headwords) != len(thelittle_items):
        print(f'【ERROR】The Little 辞典 加载失败{len(thelittle_headwords)}, {len(thelittle_items)}')
        os._exit(-1)
    if biaoxianwenxing_flag and len(biaoxianwenxing_headwords) != len(biaoxianwenxing_items):
        print(f'【ERROR】表现文型 加载失败{len(biaoxianwenxing_headwords)}, {len(biaoxianwenxing_items)}')
        os._exit(-1)
    # print(f'Loading 柯林斯高阶双解辞典 ... Total Entries: {len(collins_headwords)}')
    # print(f'Loading 牛津高阶辞典 ... Total Entries: {len(oxford_headwords)}')
    # print(f'Loading The Little 辞典 ... Total Entries: {len(thelittle_headwords)}')
    # print(f'Loading 表现文型 ... Total Entries: {len(biaoxianwenxing_headwords)}')

init()

def collins_GetVocab(queryWord):

    # 查词，返回单词和html文件
    if queryWord.encode() not in collins_headwords:
        print(f'{queryWord} Not exists in dict')
        return None
    wordIndex = collins_headwords.index(queryWord.encode())
    word, html = collins_items[wordIndex]
    word, html = word.decode(), html.decode()
    
    # 从html中提取需要的部分。
    doc = pq(html)
    with open("x.html", 'w+', encoding='utf-8') as fp:
        fp.write(doc.html())
    query_res = []
    wordDesc = doc('div[class="C1_explanation_item"]')
    for it in wordDesc.items():
        header = it('div[class="C1_explanation_box"]')
        attr = header('span[class="C1_explanation_label"]').text().replace('\n','').strip()
        mean = header('span[class="C1_text_blue"]').text().replace('\n','').strip()
        sentences = [sentence.text().replace('\n','|').strip() for sentence in list(it('li').items())[:2]]
        if attr and mean and len(sentences) > 0:
            query_res.append([queryWord, attr, mean, sentences])
    return query_res

def oxford_GetVocab(queryWord, query_res):
    
    # 查词，返回单词和html文件
    if queryWord.encode() not in oxford_headwords:
        print(f'{queryWord} Not exists in dict')
        return None
    wordIndex = oxford_headwords.index(queryWord.encode())
    word, html = oxford_items[wordIndex]
    word, html = word.decode(), html.decode()
    
    # 从html中提取需要的部分。
    doc = pq(html)
    with open("x.html", 'w+', encoding='utf-8') as fp:
        fp.write(doc.html())
    query_res['word'] = queryWord
    query_res['spell'] = ''
    query_res['example'] = []
    for wd in doc('div[id="entryContent"]').items():
        word_src = wd('h1[class="headword"]').text().strip()
        if word_src != queryWord:
            print(f'{queryWord} Not Correct in dict')
            return None
        word_attr = wd('span[class="pos"]').text().strip()
        word_spell = list(wd('span[class="phon"]').items())[0].text().strip()
        query_res['spell'] += f'[{word_attr}]{word_spell} '
        
        for word_desc in wd('div[class="entry"] > ol > li[class="sense"]').items():
            word_mean_en = word_desc('span[class="def"]').text().strip()
            word_mean_ch = '[{}] {}'.format(word_attr, word_desc('deft').text().strip())
            sentence_en = [sen.text().strip() for sen in word_desc('ul[class="examples"] li span[class="x"]').items()]
            sentence_ch = [sen.text().strip() for sen in word_desc('ul[class="examples"] li chn').items()]
            query_res['example'].append([word_mean_en, word_mean_ch, sentence_en, sentence_ch])
    return query_res

def thelittle_GetVocab(queryWord, query_res):
    
    # 查词，返回单词和html文件
    if queryWord.encode() not in thelittle_headwords:
        print(f'{queryWord} Not exists in dict')
        return None
    wordIndex = thelittle_headwords.index(queryWord.encode())
    word, html = thelittle_items[wordIndex]
    word, html = word.decode(), html.decode()
    
    # 从html中提取需要的部分。
    doc = pq(html)
    # with open("x.html", 'w+', encoding='utf-8') as fp:
    #     fp.write(doc.html())
    query_res['word'] = queryWord
    query_res['spell'] = doc('span[class="ipa"]').text().replace('\n', '').strip()
    query_res['mean'] = doc('div[class="coca2"]').text().replace('\n', '').strip()
    return query_res

# 查词，返回单词和html文件
def query_word(headwords, items, queryWord):
    if queryWord.encode() not in headwords:
        print(f'{queryWord} Not exists in dict')
        return None, None, False
    wordIndex = headwords.index(queryWord.encode())
    word, html = items[wordIndex]
    word, html = word.decode(), html.decode()
    return word, html, True

def biaoxianwenxing_GetVocab(queryWord, query_res):

    word, html, ok = query_word(biaoxianwenxing_headwords, biaoxianwenxing_items, queryWord)
    if not ok:
        return query_res
    
    query_res['queryWord'] = queryWord
    
    # 从html中提取需要的部分。
    doc = pq(html)
    
    query_res['link'] = []
    while True:
        print("word", word)
        query_res['link'].append(queryWord)
        if '@@@LINK=' not in doc.html():
            break
        queryWord = doc.html().split('=')[1].strip()
        word, html, ok = query_word(biaoxianwenxing_headwords, biaoxianwenxing_items, queryWord)
        if not ok:
            return query_res
        doc = pq(html)
        
    # with open("result/y.html", 'w+', encoding='utf-8') as fp:
    #     fp.write(doc.html())    
    
    query_res['word'] = []
    wordBlock = list(doc('h1').items())
    for word in wordBlock:
        word = word.text().replace('\n', '').strip()
        query_res['word'].append(word)
        # print(f'word: {word}')
        
    if len(query_res['word']) > 1:
        print(f"{queryWord} word size > 1. {query_res['word']}")
    
    query_res['chinese_meaning'] = []
    meaningBlock = list(doc('p[class="meaning"]').items())
    startIdx = 2 if len(meaningBlock) % 4 == 0 else 1
    step = 4 if len(meaningBlock) % 4 == 0 else 3
    for meaning in meaningBlock[startIdx::step]:
        meaning = meaning.text().replace('\n', '').strip()
        query_res['chinese_meaning'].append(meaning)
        # print(f'chinese_meaning: {meaning}')
    
    query_res['connect'] = []
    connectBlock = list(doc('div[class="connectionBlock"] > table > tr > td').items())
    for connect in connectBlock:
        connect = connect.text().replace('\n', '').strip()
        query_res['connect'].append(connect)
        # print(f'connect: {connect}')
    # if len(connectBlock) >= 1:
    #     connect = connectBlock[0].text().replace('\n', '').strip()
    #     query_res['connect'] = connect
    #     # print(f'connectBlock: {connect}')
        
    query_res['explanation'] = []
    explanationBlock = list(doc('p[class="c-honbun"]').items())
    for explanation in explanationBlock:
        explanation = explanation.text().replace('\n', '').strip()
        # 判断是否以数字为开头
        if explanation[0].isdigit():
            explanation = explanation[2:]
        query_res['explanation'].append(explanation)
    explanationBlock = list(doc('p[class="c-honbun-1para"]').items())
    for explanation in explanationBlock:
        explanation = explanation.text().replace('\n', '').strip()
        query_res['explanation'].append(explanation)

    query_res['example'] = []
    exampleBlock = doc('div[class="exampleBlock"] > dl > dd')
    for example in exampleBlock.items():
        rt_tags = example('rt')
        for rt_tag in rt_tags.items():
            rt_tag.remove()
            ## 替换文本，两边包裹括号
            # rt_tag.replace_with(f'({rt_tag.text()})')
        text = example.text().replace('\n', '').strip()
        query_res['example'].append('△ ' + text)
        # print(f'example: {text}')

    return query_res

if __name__ == '__main__':
    # print(oxford_GetVocab(queryWord="aboveboard"))
    # print(biaoxianwenxing_GetVocab(queryWord="うえで", query_res={}))
    print(biaoxianwenxing_GetVocab(queryWord="にわたって", query_res={}))