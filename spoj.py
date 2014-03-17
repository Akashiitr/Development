#Program to check question done by one user and not the other on spoj

import sys
import urllib2
import webbrowser

#Function to find all occurences of a substring
def find_all(strin,sub1,sub2):
	i=j=0
	while True:
		i=strin.find(sub1,i)
		j=strin.find(sub2,j)
		if i==-1 or j==-1:
			return
		#Condition because sometimes there are some empty strings. Spoj Errors--can't do anything about it
		if i+3!=j:
			yield strin[i+3:j]
		i+=len(sub1)
		j+=len(sub2)

recently = []
recent_code = []
#Function to print recent questions
def recent():
	url = "http://www.spoj.com/problems/classical/sort=-5"
	req = urllib2.Request(url)
	try:
		response = urllib2.urlopen(req)
	except:
		print "Check Your internet connection"
	html = response.read()
	ix = html.find('<tr class="problemrow">')
	count = 0
	while count < 10:
		fix = html.find('<b>', ix)
		fix += 3
		lix = html.find('</b>', fix) 
		recently.append(html[fix:lix])
		ix = html.find('<tr class="problemrow">',lix)
		fix = html.find('/problems',ix)
		fix += 10
		lix = html.find(">",fix)
		lix -= 2
		recent_code.append(html[fix:lix])
		count += 1

if len(sys.argv) < 3:
	#pirnt "Usage : python spoj.py <username1> <username2>"
	exit()

#Creating the urls and request objects

url1="http://www.spoj.com/users/"+sys.argv[1]+"/"
req1=urllib2.Request(url1)

url2="http://www.spoj.com/users/"+sys.argv[2]+"/"
req2=urllib2.Request(url2)

#Fetching the request created in the previous step
try:
	response1=urllib2.urlopen(req1)
	response2=urllib2.urlopen(req2)
except urllib2.HTTPError as e:
	print "The server did not reply"
	exit()
except urllib2.URLError as e:
	print "Given URL not found"
	exit()

#Getting the page source of the webpages
html1=response1.read()
html2=response2.read()

#Raising an exception and exiting program if any of the usernames is not found
try:
	temp1=html1.count(sys.argv[1])
	temp2=html2.count(sys.argv[2])
	if temp1<4 or temp2<4:
		raise Exception("Wrong usernames")
except:
	print "Make sure you have entered the correct usernames"
	exit()

#Isolating the area where the problem ID's are stored by finding the first and the last index
try:
	index1=html1.index('<p align="left">')
	lastindex1=html1.rfind('<p align="left">')
	
	index2=html2.index('<p align="left">')
	lastindex2=html2.rfind('<p align="left">')
except:
	print "There was an error. Make sure you have entered the correct spoj username"
	exit()

#Creating a string for the contents of the table and searching for problem ID's in it
table1=html1[index1:lastindex1-1]
start1=find_all(table1,'/">','</a>')

table2=html2[index2:lastindex2-1]
start2=find_all(table2,'/">','</a>')

#Taking the difference of the two lists containing the questions ID's done by username1
#and not by username2 and then sorting.
diff=list(set(start1)-set(start2))
diff.sort()
for item in diff:
	print item
for item in list(set(start2)):
	print item 


#Problem Classifier
url_classf = "http://problemclassifier.appspot.com/index.jsp?search=+ABCDEF&usr="
req_classf = urllib2.Request(url_classf)
try:
	response_classf=urllib2.urlopen(req_classf)
except:
	print "Check your internet Connection"
html_classf = response_classf.read()
tagged = []
for item in diff:
	check = "http://www.spoj.pl/problems/" + item
	ix = html_classf.find(check)
	if ix != -1:
		fix = html_classf.find('<td width=650>',ix)
		fix += 15
		lix = html_classf.find('</td>',fix)
		classf = html_classf[fix:lix]
		classf = item + "   --    " + classf
		tagged.append(classf)
	else:
		tagged.append(item)

#Using a for-in loop for printing each problem ID with tag (if any) in a different line 
x = 1
for item in tagged:
	print "%d. %s"%(x,item)
	x += 1

#And that's how you would know how far are you from them
print "Number of questions : ",len(diff)

#Giving option to open a particular question
try:
	while True:
		print "Press the Number of Question want to open or press 0 to check recently added questions: "
		num = int(raw_input())
		if num == 0:
			recent()
			x = 1
			for item in recently:
				print "%d. %s"%(x, item)
				x += 1
			print "Press the Number of Question want to open"
			num = int(raw_input())
			url3 = "http://www.spoj.com/problems/"+recent_code[num-1]+"/"
			webbrowser.open_new_tab(url3)
		else :
			url3 = "http://www.spoj.com/problems/"+diff[num-1]+"/"
			webbrowser.open_new_tab(url3)
except:
	print "Make Sure you have internet Connection"


