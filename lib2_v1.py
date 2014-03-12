import urllib2, StringIO, sys, urllib
from lxml import etree
from BeautifulSoup import BeautifulSoup

def get_html(url):

	try:
		proxy = urllib2.ProxyHandler({'http': 'http://f2010181:rzw20gf@10.1.9.36:8080'})
		auth = urllib2.HTTPBasicAuthHandler()
		opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
		urllib2.install_opener(opener)
		request = urllib2.Request(url)
		request.add_header("User-Agent","Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101")
		html = urllib2.urlopen(request).read()
		return html
	except:
		print "Error accessing: ", url
	return None

i = 0
c = 0
prev = ''
print ''
fp = open('out.txt','a')
with open("final2.txt") as fileobcurr_deltaect:
	for inp in fileobcurr_deltaect:
		l = inp.split(';')
		title = l[0].strip()
		isbn = l[3].replace('-','').strip()
		author_name = l[1].split(',')[0].strip()
		date = l[2].strip()
		cc = "http://catalog.loc.gov/cgi-bin/Pwebrecon.cgi?DB=local&Search_Arg="
		nxt = "&Search_Code=GKEY%5E*&CNT=100&hist=1&type=quick"
		url_t = cc + title.replace(' ','+') + nxt
		url_is = cc + isbn + nxt
		# 1st attempt to search by isbn
		html_is = get_html(url_is)
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO.StringIO(html_is), parser)
		test = tree.xpath("//div[@class='nohits']/div[@class='nohits-left']/strong/text()")
		if test != []:
			if 'no' in test[0]:
				# attempt search by title---no results by isbn
				html_t = get_html(url_t)
				parser = etree.HTMLParser()
				tree = etree.parse(StringIO.StringIO(html_t), parser)
				# now test for title no results
				test = tree.xpath("//div[@class='nohits']/div[@class='nohits-left']/strong/text()")
				if test != []:
					print 'No Details: ',title
					continue
				else:
					authors_loc = []
					year_loc = []
					links_loc = []
					
					#Top 10 results
					print "Details : ",title
					# now u have choosen title
					# test for no results here

					#----

					for i in xrange(1,10):
						au = "//tr[%i]/td[3]/text()" % (2*i)
						ye = "//tr[%i]/td[5]/text()" % (2*i)
						li = "//tr[%i]/td[4]/a/@href" % (2*i)
						n = tree.xpath(au)	#auth
						y = tree.xpath(ye)	#year
						l = tree.xpath(li)	#link
						if y == [] or n== []:
							continue
						#print author_name, n[0]
						if author_name in n[0]:
							authors_loc.append(n[0].strip('\n').split(',')[0])
							year_loc.append(y[0].strip('\n'))
							links_loc.append(l[0])

					ind = 0
					min_delta = abs(int(year_loc[0])-int(date))

					for i in xrange(len(year_loc)):
						curr_delta = int(year_loc[i]) - int(date)
						if curr_delta == 0:
							ind = i
							break
						elif curr_delta > 0:
							if curr_delta < min_delta:
								min_delta = curr_delta
								ind = i
					print year_loc[ind], authors_loc[ind]

					#print authors_loc
					#print year_loc
					#print links_loc,'\n'
		else:
			print 'ISBN direct',isbn



