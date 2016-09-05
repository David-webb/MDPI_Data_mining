#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this py is used to analysis the submission data from mdpi
import pandas as pd
from scipy import stats as ss
import matplotlib.pyplot as plt

import seaborn as sns

# Reading data from web
data_url = "https://raw.githubusercontent.com/alstat/Analysis-with-Programming/master/2014/Python/Numerical-Descriptions-of-the-Data/data.csv"
df = pd.read_csv('data.csv')

print df.head()

print df.tail()

print df.columns

print df.index
#print df.T

print df.ix[10:20, 0:3]

print df.describe()

print ss.ttest_1samp(a = df.ix[:, 'Abra'], popmean = 15000)

print ss.ttest_1samp(a = df, popmean = 15000)

#plt.show(df.plot(kind = 'box'))

pd.options.display.mpl_style = 'default' # Sets the plotting display theme to ggplot2
#plt.show(df.plot(kind = 'box'))
#plt.show(sns.boxplot(df))
#plt.show(sns.distplot(df.ix[:,2], rug = True, bins = 15))
#with sns.axes_style("white"):
#    plt.show(sns.jointplot(df.ix[:,1], df.ix[:,2], kind = "kde"))

#plt.show(sns.lmplot("Benguet", "Ifugao", df))
