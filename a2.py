#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: renpp
# @Desc: { 模块描述 }
# @Date: 2023/02/09 15:44
# @Script: a2.py


import sys
import argparse
import re
import pandas as pd


def parse_args():
    """ """
    parser = argparse.ArgumentParser(description="deal raw count file to count matrix file")
    parser.add_argument("-c", "--count", type=str, required=True, help="input raw count file")
    parser.add_argument("-o", "--output", type=str, required=True, help="output final count file")
    parser.add_argument("-f", "--filter", type=int, default=2, help="default 2")
    args = parser.parse_args()
    return args


def fun1(count, output):
    pass

def fun2(i,o):
    pass


def main():
    args = parse_args()
    fun1(args.count, args.output)


if __name__ == '__main__':
    main()
