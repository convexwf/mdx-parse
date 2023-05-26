# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project : mdx-parser
# @FileName : __init__.py
# @Author : convexwf@gmail.com
# @CreateDate : 2023-05-23 16:06
# @UpdateTime : 2023-05-26 19:06

from .moji_reader import MojiReader
from .shogakukan_reader import ShogakukanReader

__all__ = ["MojiReader", "ShogakukanReader"]
