#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Author: renpp
# @Desc: { common code Test }
# @Date: 2023/02/10 9:16
# @Script: main.py

from collections import defaultdict, Counter
from common import Seq, Read_file
import pandas as pd
import numpy as np
import joblib
import matplotlib.pyplot as plt

#Seq类-数据
DNA = "ATGCGCatccgTTGGccAAACTTGACTA"
seq = Seq(DNA)
#Seq类-方法
s1 = seq.revcom()
s2 = seq.reverse()
s3 = seq.complement()
s4 = seq.atgc()
s5 = seq.repeat()

#Read_file类 - 数据
f = Read_file("genome.fa")
#Read_file类-方法
#a = f.read_fasta()
a = f.read_fastq()
for k1, k2, k3, k4  in a:
    print(k1, k2, k3, k4)

