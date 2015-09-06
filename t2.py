#!/usr/bin/env python
from __future__ import print_function
import urllib2
from BeautifulSoup import BeautifulSoup
import time
import datetime
import sys
from dateutil.relativedelta import relativedelta

fi = open("t",'r')
text = fi.readlines()
t=0
print('<table border="1">')
print('<tr>')
print('<th>Number</th>')
print('<th>Description</th>')
print('</tr>')
for i in text:
	#print i
        print('<tr>')
	a = i.strip().replace('\"', '\'').split("#")
        soup = BeautifulSoup(urllib2.urlopen('http://bugs.winehq.org/show_bug.cgi?id={0}'.format(a[1])))
        time_txt = soup.find(None, {"class": "bz_comment_time"}).text
        time_str = time.strptime(time_txt[:-4],"%Y-%m-%d %H:%M:%S")
	if len(sys.argv) > 1:
		da = sys.argv[1].split('-')
		today = datetime.date(int(da[0]), int(da[1]), int(da[2]))
	else:	
        	today = datetime.date.today()
        past = datetime.date(time_str.tm_year, time_str.tm_mon, time_str.tm_mday)
        delta = relativedelta(today, past)
        delta_txt=""
        if delta.years:
                delta_txt += " {} year".format(delta.years)
                if delta.years > 1:
                        delta_txt +='s'

        if delta.months:
                delta_txt += " {} month".format(delta.months)
                if delta.months> 1:
                        delta_txt +='s'
                        
        if delta.days:
                delta_txt += " {} day".format(delta.days)
                if delta.days> 1:
                        delta_txt +='s'
                        
        print('<td><a href="http://bugs.winehq.org/show_bug.cgi?id={0}" title="Age:{2}">{0}</a></td><td>{1}</td>'.format(a[1], a[2], delta_txt))
        print('</tr>')

print('</table>')
