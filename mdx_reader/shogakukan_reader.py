# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : mdx-parser
# @FileName : shogakukan_reader.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-05-26 19:06
# @UpdateTime : 2023-05-26 19:06

from .base_reader import BaseMDXReader
from pyquery import PyQuery as pq


class ShogakukanReader(BaseMDXReader):

    mdx_file_path = "dict/小学馆V3日汉辞典_20220623/小学馆V3日汉辞典.mdx"

    @classmethod
    def search(cls, query_word: str):
        is_found, result_list = cls._search(query_word)

        if not is_found:
            return False, []

        query_list = []
        for result in result_list:
            query_result = dict()
            query_result["word"] = []
            query_result["link"] = []
            query_result["meaning"] = []
            query_result["content"] = []

            doc = pq(result)

            # extract pages link, maybe more than one
            _query_word = query_word
            while True:
                query_result["link"].append(_query_word)
                if "@@@LINK=" not in doc.html():
                    break
                _query_word = doc.html().split("=")[1].strip()
                is_found, _result = cls._search(_query_word)
                if not is_found:
                    return True, [query_result]
                doc = pq(_result[0])

            # extract word, maybe more than one
            word_block = list(doc("h3").items())
            for word in word_block:
                word_text = word.text().strip()
                word_spell_block = word('span[class="pinyin_h"]')
                if word_spell_block:
                    word_spell = word_spell_block.text().strip()
                    word_text = word_text.replace(word_spell, f"【{word_spell}】")
                query_result["word"].append(word_text)
            if len(query_result["word"]) > 1:
                print(f"{_query_word} word size > 1. {query_result['word']}")

            for p_block in doc("section > p").items():
                if p_block.attr("data-orgtag") == "meaning":
                    meaning = p_block.text().replace("\n", "").strip()
                    query_result["meaning"].append(meaning)
                    query_result["content"].append([meaning])
                elif p_block.attr("data-orgtag") == "example":
                    query_result["content"][-1].append(
                        p_block.text().replace("\n", "/").strip()
                    )
            query_list.append(query_result)
        return True, query_list
