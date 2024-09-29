# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : mdx-parse
# @FileName : base_reader.py
# @Author : convexwf@gmail.com
# @CreateDate : 2024-09-28 10:44
# @UpdateTime : TODO

from abc import ABC, abstractmethod
import os
from readmdict import MDX


class BaseMDXReader(ABC):

    mdx_file_path = ""
    is_initialized = False
    headwords = []
    items = []

    @classmethod
    def __init_engine(cls):
        if cls.is_initialized:
            return
        print(f"Initializing {cls.__name__} MDX engine with file: {cls.mdx_file_path}")
        if not os.path.exists(cls.mdx_file_path):
            raise FileNotFoundError(f"MDX file not found: {cls.mdx_file_path}")
        mdx_engine = MDX(cls.mdx_file_path)
        cls.headwords = [*mdx_engine]
        cls.items = [*mdx_engine.items()]
        if len(cls.headwords) != len(cls.items):
            raise ValueError("The number of headwords and items are not equal")
        cls.is_initialized = True

    @classmethod
    def _search(cls, query_word: str):
        if not cls.is_initialized:
            cls.__init_engine()
        if query_word.encode("utf-8") not in cls.headwords:
            return False, ""
        index = cls.headwords.index(query_word.encode("utf-8"))
        return True, cls.items[index][1].decode("utf-8")
