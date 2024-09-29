# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : mdx-parse
# @FileName : moji_reader.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-09-28 13:13
# @UpdateTime : TODO

from .base_reader import BaseMDXReader
from pyquery import PyQuery as pq


class MojiReader(BaseMDXReader):

    mdx_file_path = "dict/moji辞书_20190604/moji辞书.mdx"

    @classmethod
    def search(cls, query_word: str):
        is_found, result = cls._search(query_word)
        if not is_found:
            return False, []

        query_list = []
        query_result = dict()
        query_result["word"] = []
        query_result["link"] = []
        query_result["type"] = []
        query_result["meaning"] = []
        query_result["content"] = []

        # extract pages link, maybe more than one
        doc = pq(result)
        while True:
            query_result["link"].append(query_word)
            if "@@@LINK=" not in doc.html():
                break
            query_word = doc.html().split("=")[1].strip()
            is_found, result = cls._search(query_word)
            if not is_found:
                return True, [query_result]
            doc = pq(result)

        # extract word, maybe more than one
        word_block = list(doc("h3").items())
        for word in word_block:
            word = word.text().replace("\n", "").strip()
            query_result["word"].append(word)
        if len(query_result["word"]) > 1:
            print(f"{query_word} word size > 1. {query_result['word']}")

        cixing_block = list(doc('div[class="cixing"] > div').items())
        if len(cixing_block) == 0:
            seealso_block = doc('div[class="seealso"] > a').items()
            for seealso in seealso_block:
                seealso_word = seealso.text().replace("\n", "").strip()
                query_list.extend(cls.search(seealso_word)[1])
            return True, query_list

        word_type = ""
        for div in cixing_block:
            if div.attr("class") == "cixing_title":
                word_type = "『{}』".format(div.text().replace("\n", "").strip())
                query_result["type"].append(div.text().replace("\n", "").strip())
            elif div.attr("class") == "explanation":
                meaning = "{}{}".format(word_type, div.text().replace("\n", "").strip())
                query_result["meaning"].append(meaning)
                query_result["content"].append([meaning])
            elif div.attr("class") == "sentence":
                query_result["content"][-1].append(
                    div.text().replace("\n", "/").strip()
                )

        query_list.append(query_result)
        return True, query_list
