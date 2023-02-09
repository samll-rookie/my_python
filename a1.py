#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: renpp
# @Desc: { 模块描述 }
# @Date: 2023/02/06 17:00
# @Script: a1.py

import sys
import argparse
import re


def parse_args():
    """
    :return:进行参数的解析
    """
    parser = argparse.ArgumentParser(description = "deal raw count file to count matrix file")
    parser.add_argument("-i", "--count",  type =str, required=True, help="input raw count file")
    parser.add_argument("-o", "--output", type =str, required=True, help="output final count file")
    parser.add_argument("-f", "--filter", type =int, default = 2,   help="default 2")
    args = parser.parse_args()
    return args
if __name__ == '__main__':
    args = parse_args()