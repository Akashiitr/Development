#Program to sort a particular question By memory

import sys
import urllib2
import webbrowser



if len(sys.argv) < 2:
	print "Usage : python spoj_sort_mem.py <problem_id>"
	exit()
mct = 0
page = 0

element = []
while mct <= 38:
	p = str(page)
	url1 = "http://www.spoj.com/ranks/" + sys.argv[1] +"/start=" + p
	req1 = urllib2.Request(url1)
	try:
		response1 = urllib2.urlopen(req1)
	except:
		print "Make sure your have internet connection"
	html1 = response1.read()

	count = 0
	i = 0
	while count < 20:

		i = html1.find('<td><a href="/users', i)
		i =	html1.find('statusmem', i)
		i = html1.find('</td>', i)
		i = i - 10
		ch = html1[i:i+3].strip()
		#print "%d. %s"%(count,html1[i:i+3].strip())
		try:
			element.append(float(ch))
		except:
			print "koi na"
		count += 1 

	mct += 1
	page += 20
element = list(element)
element.sort()

i = 0
while i <= 40:
	print element[i]
	i += 1