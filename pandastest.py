from pandas import Series, DataFrame
import pandas as pd

obj = Series([4,7,-5,3])

print obj

obj2 = Series([4, 7, -5, 3], index=['a', 'b', 'c', 'd'])

print obj2

print obj2.index

print obj2['a']
print obj2[['c','d']]
print obj2[obj2 > 0]

print 4 in obj2.values

sdata = {'Ohio': 35000, 'Texas': 71000, 'Oregon': 16000, 'Utah': 5000}
obj3 = Series(sdata)
print obj3

data = {'state': ['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year': [2000, 2001, 2002, 2001, 2002],
        'pop': [1.5, 1.7, 3.6, 2.4, 2.9]}
frame = DataFrame(data)

print frame
