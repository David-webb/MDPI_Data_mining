# -*- coding: utf-8 -*-
import os
from MdpiPapers.MdpiDBop import *

def testContinue():
    td = MdpiMysql("localhost", "root", "tw2016941017", "MDPIArticleInfo")
    return td.getControlInfo()
    pass

count = 0
while(testContinue()):
    os.system('python LetsDownload.py')
    print '\n第' + `count` + '次启动...'
    count += 1
