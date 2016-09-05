#!/usr/bin/python
# -*- coding: UTF-8 -*-

# this py is used to analysis the submission data from mdpi

import pandas as pd
import numpy as np
import pandas.io.data
import matplotlib.pyplot as plt
import os
import datetime
import time
import lunardate
from umalqurra.hijri_date import HijriDate

import seaborn as sns
from pylab import *

'''
0 : 'doi:10.3390/10010003'
1 : Chemistry & Materials Science
2 : Macromolecules Applied to Pharmaceutical Chemistry
3 : Molecules 2005, 10(1), 3-5
4 : 15 September 2004
5 : Not recorded
6 : Not recorded
7 : 31 January 2005
8 : {"Departamento de Farmacia, Facultad de Ciencias Bioquim\u00edcas y Farmace\u00faticas, Universidad Nacional de Rosario, Suipacha 531, 2000. Rosario, Argentina": ["Claudio J. Salomon"]}

'''



def isLeapYear(year):
    """判断闰年"""
    return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0

def daysInMonth(year, month):
    """ 输出某一月份的天数"""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    else:
        if isLeapYear(year):
            return 29
        else:
            return 28

def isLegalDate(year, month, day):
    """判断输入的日期是否合法"""
    if year < 1:
        return False
    elif month not in range(1, 13):
        return False
    elif day < 1 or day > daysInMonth(year, month):
        return False
    else:
        return True
    pass

def nextDay(year, month, day):
    """计算指定日期的下一天（假设给定的日期合法）"""
    if day < daysInMonth(year, month):
        return year, month, day + 1
    else:
        if month == 12:
            return year + 1, 1, 1
        else:
            return year, month + 1, 1

def dateIsBefore(year1, month1, day1, year2, month2, day2):
    """
    1. 假定给定的日期都是合法的
    2. Returns True if year1-month1-day1 is before year2-month2-day2. Otherwise, returns False.
    """
    if year1 < year2:
        return True
    if year1 == year2:
        if month1 < month2:
            return True
        if month1 == month2:
            return day1 < day2
    return False

def daysBetweenDates(year1, month1, day1, year2, month2, day2):
    """
    1. Returns the number of days between year1/month1/day1 and year2/month2/day2.
    2. Assumes inputs are valid dates in Gregorian calendar.
    """
    # program defensively! Add an assertion if the input is not valid!
    assert not dateIsBefore(year2, month2, day2, year1, month1, day1)
    days = 0
    while dateIsBefore(year1, month1, day1, year2, month2, day2):
        year1, month1, day1 = nextDay(year1, month1, day1)
        days += 1
    return days

def getLocation(auth):
    """获取作者单位中的国家信息"""   # 函数的正确性需要进一步检查！！！！！！！！！！！！！！1
    # print type(auth)
    if auth == 'affiliations Info Not Given!':
        return 'None'
    ad = eval(auth)
    res = []
    for aff in ad:
        cn = aff.split(',')[-1].strip()
        if cn.isdigit():
            cn = aff.split(',')[-2].strip()
        cn = cn.split(' ')[-1]
        # if cn=='Republic':
            # print aff
        # print cn
    aa = '100086'
    #print aa.isdigit()
    return cn


def getTime(t, tp='w'):
    """
    1. 从给定的日期字符串中获取对应的年月日或星期
    2. 参数t：日期字符串； 参数 tp： 读取模式（可选y/m/d/w, 默认w(星期)）
    """
    # print t
    mon = {'January': 1}
    if t == 'Not recorded':
        return 'None'
    else:
        date_time = datetime.datetime.strptime(t, '%d %B %Y')
        w = date_time.weekday()
        m = date_time.month
        d = date_time.day
        y = date_time.year
        # print w,m,t
        if tp == 'y':
            return y
        elif tp == 'm':
            return m
        elif tp == 'd':
            return d
        elif tp == 'w':
            return w
    pass


def getChinaTime(t):
    """将输入的日期字符串转换成中国的阴历日期(这里只输出月份)"""
    # print t
    if t == 'Not recorded':
        return 'None'
    else:
        date_time = datetime.datetime.strptime(t, '%d %B %Y')
        m = date_time.month
        d = date_time.day
        y = date_time.year
        # print w,m,t
        ld = lunardate.LunarDate.fromSolarDate(y, m, d)
        # print ld,ld.month,m
        return ld.month
    pass


def getAribaTime(t):
    """将日期字符串转换成阿拉伯日期"""
    # print t
    if t == 'Not recorded':
        return 'None'
    else:
        date_time = datetime.datetime.strptime(t, '%d %B %Y')
        w = date_time.weekday()
        m = date_time.month
        d = date_time.day
        y = date_time.year
        # print w,m,t
        ld = HijriDate(y, m, d, gr=True)
        # print ld,ld.month,m
        return ld.month
    pass


def getChinaHoliday(t):
    """找出距离输入日期最近的中国节日，输出距离的天数"""
    date_time = datetime.datetime.strptime(t, '%d %B %Y')
    y = date_time.year
    # 中国阳历节日
    sh = [
          (y, 1, 1),    # 元旦
          (y, 4, 5),    # 清明
          (y, 5, 1),    # 五一劳动节
          (y, 10, 1)    # 国庆节
          ]
    # 中国阴历节日
    lh = [
          (y, 1, 1),    # 大年初一（春节）
          (y, 5, 5),    # 端午节
          (y, 8, 15)    # 中秋节
    ]
    res = 365
    for h in sh:
        hd = datetime.datetime(h[0], h[1], h[2], 0, 0, 0)
        ds = (date_time-hd).days
        if abs(ds) < res:       # 距离输入的日期最近的阳历节日
            res = abs(ds)

    for h in lh:
        ld = lunardate.LunarDate(h[0], h[1], h[2], 0).toSolarDate()
        hd = datetime.datetime(ld.year, ld.month, ld.day, 0, 0, 0)
        ds = (date_time-hd).days
        if abs(ds) < res:       # 距离输入的日期最近的阴历节日
            res = abs(ds)
    # print t,res
    return res
    pass


def getUSAHoliday(t):           # 功能不完善！！！！！！！！！！！！！！
    date_time = datetime.datetime.strptime(t, '%d %B %Y')
    y = date_time.year
    m = date_time.month
    d = date_time.day
    if m == 8:
        # print y,d
        return d
    elif m == 9:
        return 31 + d
    # print t,res
    return 0
    pass


def outimg0525(df, cn):
    imgpath = 'img'
    usadf = df[df[8].str.contains(cn)]
    print cn, len(usadf)
    cc1 = usadf[4].apply(getUSAHoliday)
    #print type(cc1)
    cc = cc1[cc1 != 0].value_counts().sort_index()
    plt.figure(figsize=(16, 6), dpi=75)
    cc.plot(kind='bar')

    imgname = os.path.join(imgpath, cn + '_sm_8_9.png')

    plt.savefig(imgname,  dpi=75)
    plt.clf()
    pass

def getChineseNewYear(t):
    date_time = datetime.datetime.strptime(t,'%d %B %Y')
    y = date_time.year
    m = date_time.month
    d = date_time.day
    ldate = lunardate.LunarDate.fromSolarDate(y, m, d)
    lm = ldate.month
    ld = ldate.day
    if lm == 4:
        #print y,d
        return ld
    elif lm == 5:
        return 30+ld
        #return 0
    #print t,res
    return 0
    pass

contries = ['USA','China','Italy','Germany','Japan','Spain','Korea','UK','Taiwan','Canada','Australia','France','Brazil','Switzerland','Malaysia','Poland','Netherlands','Sweden','Turkey','Mexico','Belgium','Portugal','Austria','India','Czech','South Africa','Greece','Denmark','Arabia','Finland','Norway','Russia','Zealand','Romania','Argentina','Egypt','Iran','Ireland','Thailand','Israel','Singapore','Chile','Hungary','Pakistan','Slovenia','Serbia','Colombia','Croatia','Slovakia','Lithuania','Morocco','Hong Kong','Indonesia','Nigeria','Jordan','Maroc','Vietnam','Tunisia','Bulgaria','Algeria','Bangladesh','Iraq','Cyprus','Kenya','Brasil']


def outimg(df,cn):
    imgpath = 'img'
    usadf = df[df[8].str.contains(cn)]
    cc = usadf[4].apply(getTime).value_counts(sort=False).sort_index()
    #print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    imgname = os.path.join(imgpath,cn+'_week.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()
    pass



def loaddata():
    #df = pd.read_csv('out.csv',header=None,nrows=20)
    df = pd.read_csv('out.csv',header=None,nrows=200000)
    df = df[df[4] != 'Not recorded']
    l,t = df.shape
    print l,t
    for i in range(l):
        for j in range(t):
            #print j,':',df[j][i]
            pass
    for a in df[8]:
        #print a
        #getLocation(a)
        pass
    print df[1].value_counts()
    #print df[[1,4,8]]
    for cn in contries:
        print cn
        #outimg(df,cn)

        #print c, len(df[df[8].str.contains(c)][8])
    print len(df[df[8].str.contains('USA')][8])
    print len(df[df[8].str.contains('Hong Kong')][8])
    #for cn in df[8].apply(getLocation).value_counts().index:
        #print cn

    usadf = df[df[8].str.contains('China')]
    cc = usadf[4].apply(getChinaHoliday).value_counts().sort_index()
    print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    print usadf[4].apply(getChineseNewYear).mean()
    #print usadf



def loaddata0525():
    # df = pd.read_csv('out.csv',header=None,nrows=20)
    df = pd.read_csv('out.csv', header=None, nrows=200000)
    df = df[df[4] != 'Not recorded']
    l,t = df.shape
    print l,t
    for i in range(l):
        for j in range(t):
            #print j,':',df[j][i]
            pass
    for a in df[8]:
        #print a
        #getLocation(a)
        pass
    #print df[1].value_counts()
    #print df[[1,4,8]]
    k = 0
    for cn in contries:
        #print cn
        #outimg0525(df,cn)
        if k>10:
            break
        else:
            k+=1
    cnn = df[8].apply(getLocation).value_counts()
    for cn in cnn.index:
        print cn, cnn[cn]
        break
    usadf = df[df[8].str.contains('China')]
    print len(usadf)
    cc1 = usadf[4].apply(getChineseNewYear)
    print type(cc1)
    cc = cc1[cc1 != 0].value_counts().sort_index()
    cc.plot(kind='bar')
    plt.plot(cc)
    plt.show()




def testpandas():
    sym = 'BABA'
    finace = pd.io.data.DataReader(sym, 'yahoo', start='2014/11/11')
    #print finace.tail(30)
    plt.plot(finace.index, finace["Open"])
    plt.show()
    pass

def getTime0703(t,sm=7,sd=4,l=8):
    #print t
    mon = {'January':1}
    if t=='Not recorded':
        return 'None'
    else:

        date_time = datetime.datetime.strptime(t,'%d %B %Y')
        w = date_time.weekday()
        m = date_time.month
        d = date_time.day
        y = date_time.year
        #print w,m,t
        if dateIsBefore(y,m,d,y,sm,sd):
            db = daysBetweenDates(y,m,d,y,sm,sd)
            if db<l:
                return 7-db
        else:
            db = daysBetweenDates(y,sm,sd,y,m,d)
        #if db<l:
            if db<l:
                return db+7
        return -1
    pass

def loaddata0713():
    print 'oo'
    #df = pd.read_csv('out.csv',header=None,nrows=20)
    df = pd.read_csv('out.csv',header=None,nrows=200000)
    l,t = df.shape
    print l,t
    df = df[df[4] != 'Not recorded']
    l,t = df.shape
    print l,t
    df = df[df[8].str.contains('Germany')]
    l,t = df.shape
    print l,t
    res = np.zeros(15)
    for d in df[4]:
        db = getTime0703(d,12,25)
        if db!=-1:
            res[db]+=1
    print res

    pass

def getlist(cn,t,n):
    res = []
    for i in range(t):
        res.append(str(n)+cn)
    return res

def loaddata0722():
    print '0722'
    df = pd.read_csv('out.csv',header=None,nrows=200000)
    l,t = df.shape
    print l,t
    v1 = df[1].value_counts()
    print type(v1)
    print v1.index

    rc = []
    rs = []
    rn = []
    k = 9
    i = 0
    for cn in contries:
        ndf = df[df[8].str.contains(cn)]
        cdf = ndf[1].value_counts()
        #cdf[0] = cn
        #print type(cdf)
        #print cdf.values
        w = len(cdf)

        rc.extend(getlist(cn,w,i))
        rs.extend(cdf.index)
        rn.extend(cdf.values)
        i+=1
        if k<i:
            break


    data = {'subject':rc,'country':rs,'number':rn}
    frame = pd.DataFrame(data)
    print frame


    sns.set()
    #flights_long = sns.load_dataset("flights")
    flights = frame.pivot("country", "subject", "number")

    # Draw a heatmap with the numeric values in each cell
    sns.heatmap(flights, linewidths=.5)
    sns.plt.show()

# generate the plot by country
def drawCountry():
    df = pd.read_csv('out.csv',header=None,nrows=200000)
    rc = []
    #rs = []
    rn = []
    for cn in contries:
        rc.append(cn)
        ndf = df[df[8].str.contains(cn)]
        w,h = ndf.shape
        rn.append(w)
    #print rc
    #print rn
    data = {'country':rc,'number':rn}
    frame = pd.DataFrame(data)

    frame = frame.sort_values(by='number',ascending =True)

    frame.index = frame['country']

    frame['number'].plot(kind='barh')

    print frame['country']
    plt.show()

# generate the joint work between two countries
def drawJointWork():
    bigcs = ['USA','China','Germany','Italy','UK','Spain','Japan','France','Korea','Canada','Australia','Taiwan','Switzerland']
    df = pd.read_csv('out.csv',header=None,nrows=200000)
    rc1 = []
    rc2 = []
    #rs = []
    rn = []
    for c1 in bigcs:
        for c2 in bigcs:
            if c1!=c2:
                ndf = df[df[8].str.contains(c1)]
                ndf = ndf[ndf[8].str.contains(c2)]
                w,h = ndf.shape
                rc1.append(c1)
                rc2.append(c2)
                rn.append(w)

    print rn
    data = {'c1':rc1,'c2':rc2,'number':rn}
    frame = pd.DataFrame(data)
    frame = frame.sort_values(by='number',ascending =True)
    print frame


    sns.set()
    #flights_long = sns.load_dataset("flights")
    flights = frame.pivot("c1", "c2", "number")

    # Draw a heatmap with the numeric values in each cell
    sns.heatmap(flights, linewidths=.5)
    sns.plt.show()


def drawdfyear(df):

    cc1 = df[4].apply(getTime)
    cc = cc1[cc1 != 0].value_counts().sort_index()
    plt.figure(figsize=(16,6), dpi=75)
    cc.plot(kind='bar')
    plt.show()
    #imgname = os.path.join(imgpath,cn+'_sm_8_9.png')

    #plt.savefig(imgname,  dpi=75)
    #plt.clf()

    pass
#draw basic time distribution
def drawAllTime():
    df = pd.read_csv('out.csv',header=None,nrows=20000)
    rc1 = []
    rc2 = []
    bigcs = ['USA','China','Germany','Italy']
    for cn in bigcs:
        #ndf = df[df[8].str.contains(cn)]
        #drawdfyear(ndf)
        pass

    for i,j in df.groupby(df[1]):
        #print i,type(j),j.shape
        #drawdfyear(j)
        pass


def outimg_4_1_1(df):

    imgpath = 'results'
    cn = '4.1.1'
    #usadf = df[df[8].str.contains(cn)]
    cc = df[4].apply(getTime).value_counts(sort=False).sort_index()
    #print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    imgname = os.path.join(imgpath,cn+'_res.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()
    pass

def outimg_4_1_2(df,cn):

    imgpath = 'results'

    usadf = df[df[8].str.contains(cn)]
    cn = '4.1.2_'+cn
    cc = usadf[4].apply(getTime).value_counts(sort=True).sort_index()
    #print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    imgname = os.path.join(imgpath,cn+'_res.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()
    pass

def outimg_4_1_3(df):
    res = {}
    nm = 'cn_number'
    imgpath = 'results'
    print len(df)
    for cn in contries:
        usadf = df[df[8].str.contains(cn)]
        res[cn] = len(usadf)
    #print res
    cc = pd.Series(res, name='DateValue')
    #print cc
    cc = cc.sort_values(ascending=False)[:14]
    cc.plot(kind='bar')
    imgname = os.path.join(imgpath,nm+'_res.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()

def outimg_4_1_4(df):
    bigcs = ['USA','China','Germany','Italy','UK','Spain','Japan','France','Korea','Canada','Australia','Taiwan','Switzerland']
    #df = pd.read_csv('out.csv',header=None,nrows=200000)
    subjs = ['Chemistry & Materials Science','Biology & Life Sciences','Environmental & Earth Sciences','Business & Economics','Engineering','Medicine & Pharmacology','Computer Science & Mathematics','Social Sciences, Arts and Humanities','Physical Sciences']
    rc1 = []
    rc2 = []
    #rs = []
    rn = []
    for c1 in bigcs:
        for c2 in subjs:
            if c1!=c2:
                ndf = df[df[8].str.contains(c1)]
                ndf = ndf[ndf[1].str.contains(c2)]
                w,h = ndf.shape
                rc1.append(c1)
                rc2.append(c2)
                rn.append(w)

    print rn
    data = {'c1':rc1,'c2':rc2,'number':rn}
    frame = pd.DataFrame(data)
    frame = frame.sort_values(by='number',ascending =True)
    print frame


    sns.set()
    #flights_long = sns.load_dataset("flights")
    flights = frame.pivot("c1", "c2", "number")

    # Draw a heatmap with the numeric values in each cell
    sns.heatmap(flights, linewidths=.5)
    sns.plt.show()

def outimg_4_1_5(df): # draw subject

    imgpath = 'results'

    cn = '4.1.2_subj_'
    cc = df[1].value_counts(sort=True).sort_values(ascending =True)
    print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    imgname = os.path.join(imgpath,cn+'_res.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()
    pass

def outimg_4_2_1(df): # draw weekend

    imgpath = 'results'

    cn = '4.2.1'
    cc = df[4].apply(getTime).value_counts()
    #cc = wdf[1].value_counts(sort=True)#.sort_values(ascending =True)
    print cc
    cc.plot(kind='bar')
    #plt.plot(cc)
    #plt.show()
    imgname = os.path.join(imgpath,cn+'_res.png')
    plt.savefig(imgname, dpi=75)
    plt.clf()
    pass

def outimg_4_2_2(df): # draw weekend

    imgpath = 'results'
    subjs = ['Chemistry & Materials Science',
             'Biology & Life Sciences',
             'Environmental & Earth Sciences',
             'Business & Economics',
             'Engineering',
             'Medicine & Pharmacology',
             'Computer Science & Mathematics',
             'Social Sciences, Arts and Humanities',
             'Physical Sciences'
             ]

    for sub in subjs:

        cn = '4.2.1_'+sub
        ndf = df[df[1].str.contains(sub)]
        cc = ndf[4].apply(getTime).value_counts(sort=False)
        # cc = wdf[1].value_counts(sort=True)  #.sort_values(ascending =True)
        print cc
        # print type(cc)
        cc.plot(kind='bar')
        # plt.plot(cc)
        # plt.show()
        imgname = os.path.join(imgpath, cn+'_res.png')
        plt.savefig(imgname, dpi=75)
        plt.clf()
        pass

def main():
    # loaddata0525()
    #testpandas()
    #loaddata0713()
    #loaddata0722()
    #drawCountry()
    #drawJointWork()
    #drawAllTime()
    df = pd.read_csv('out.csv', header=None, nrows=200000)
    # print type(df)
    #outimg_4_1_1(df)
    cns = ['USA', 'China', 'Germany', ' Italy']
    for cn in cns:
        #outimg_4_1_2(df,cn)
        pass

    #outimg_4_1_3(df)
    #outimg_4_1_4(df)
    #drawCountry()
    outimg_4_2_2(df)



if __name__ == '__main__':
    # print range(1, 13)

    # tmpdict = {'t1':1, 't2':2}
    # for i in tmpdict:
    #     print i

    # y, m, d = (2016, 9, 4)
    # ld = lunardate.LunarDate.fromSolarDate(y, m, d)
    # print ld, ld.month

    # t = '4 September 2016'
    # date_time = datetime.datetime.strptime(t, '%d %B %Y')
    # m = date_time.month
    # print m
    # if m == 9:
    #     print 'true'
    # else:
    #     print 'False'

    main()
