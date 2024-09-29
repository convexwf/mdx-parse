# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : mdx-parse
# @FileName : mdx_reader_test.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-09-28 15:37
# @UpdateTime : TODO


import unittest
from mdx_reader import MojiReader
from pprint import pprint


class TestMojiReader(unittest.TestCase):

    def test_search_more_than_one_page(self):
        query_word = "何故"
        query_result = MojiReader.search(query_word)
        print("--------------------")
        print("Test MojiReader search more than one page")
        print("Query word:", query_word)
        pprint(query_result)
