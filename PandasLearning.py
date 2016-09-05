#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'Tengwei'

from pandas import Series, DataFrame
import pandas as pd
import numpy as np

obj = Series([1, 2, 3, 4], index=['n1', 'n2', 'n3', 'n4'])
print obj
print obj.values
print obj.index
print obj['n2']
print obj[['n1', 'n3']]
print obj > 2
print obj[obj > 2]
print obj * 2
print np.exp(obj)

for i in obj:
    print i
for i in obj.index:
    print i


# False
if 2 in obj:
    print True
else:
    print False

# True
if 'n1' in obj:
    print True
else:
    print False

# 只传递一个字典的时候，结果Series中的索引将是排序后的字典的建。
sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj2 = Series(sdata)
print obj2

# 在这种情况下， sdata 中的3个值被放在了合适的位置，但因为没有发现对应于 ‘California’ 的值，就出现了 NaN （不是一个数），这在pandas中被用来标记数据缺失或 NA 值。
# 在pandas中用函数 isnull 和 notnull 来检测数据丢失：
states = ['California', 'Ohio', 'Oregon', 'Texas']
obj3 = Series(sdata, states)
print obj3

data = [['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        [2000, 2001, 2002, 2001, 2002],
        [1.5, 1.7, 3.6, 2.4, 2.9]]
frame = DataFrame(data)
print 'frame:'
print frame[1]


