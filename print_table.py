# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : print_table
# @FileName : print_table.py
# @Author : convexwf@gmail.com
# @CreateDate : 2022-10-16 22:01
# @UpdateTime : Todo

from textwrap import wrap
import reportlab
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.pdfbase import pdfmetrics,ttfonts
import xlrd

from read_excel import read_word
from read_mdx import oxford_GetVocab, thelittle_GetVocab

pdfmetrics.registerFont (reportlab.pdfbase.ttfonts.TTFont ('song', "C:/Windows/Fonts/simfang.ttf"))  # 注册字体
pdfmetrics.registerFont (reportlab.pdfbase.ttfonts.TTFont ('arial', "arial.ttf"))

def data_wrap(data):
    results = []
    for [word, spell] in data:
        mdx_data = getVocab(word)
        if mdx_data is None:
            continue
        for it in mdx_data:
            results.append([word, spell, it[1], it[2], it[3]])
    return(results)

def print_td(data):
    results = []
    for it in data:
        results.append(it[0], it[1], it[2], it[3], '</br>'.join(it[4]))
    to_write = ['|' + ' | '.join(it) + '|\n' for it in results]
    with open('GRE.md', 'w+', encoding='utf-8') as fp:
        fp.writelines(to_write)

def vocab_wrap(data):
    results = []
    for it in data:
        result = {}
        result = thelittle_GetVocab(it, result)
        if result:
            result = oxford_GetVocab(it, result)
        if result:
            results.append(result)
    return results

def print_list(results):
    infos = [
        '# GRE',
        '',
        '[TOC]',
        '',
    ]
    for result in results:
        info = [
            f'## {result["word"]}',
            '',
            f'- mean: {result["mean"]}',
            f'- spell: {result["spell"].strip()}',
        ]
        for example in result['example']:
            info += [
                f'- {example[1]}',
                f'  {example[0]}',
                '',
            ]
            if len(example[2]) > 0:
                info += ['  ```eng']
                for sentence_en, sentence_ch in zip(example[2], example[3]):
                    info += [
                        f'  {sentence_en}',
                        f'  {sentence_ch}',
                    ]
                info += [
                    '  ```',
                    '',
                ]
        infos += info
    with open('GRE.md', 'w+', encoding='utf-8') as fp:
        fp.writelines(line + '\n' for line in infos)
    

if __name__ == '__main__':
    
    data = read_word()[:100]
    print_list(vocab_wrap(data))

    # elements = []
    # t = Table(data, [it * inch for it in [1, 1.2, 0.6, 2]], 20 * [0.2 * inch])
    # t.setStyle(TableStyle([
    #     ('TEXTCOLOR', (0, 0), (-1, -1), colors.green),
    #     ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('BOX', (0, 0), (-1, -1), 0.25, colors.black),
    #     ('FONT', (3,0), (-1,-1), 'song'),
    #     ('FONT', (0,0), (-2,-1), 'arial')
    # ]))
    # elements.append(t)
    # doc = SimpleDocTemplate('TabDemo3.pdf')
    # doc.build(elements)

