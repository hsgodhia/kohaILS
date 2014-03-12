from splinter import Browser
import urllib2, StringIO, sys
from lxml import etree
from BeautifulSoup import BeautifulSoup


def normalize_query(query):
	return query.strip().replace(":","%3A").replace("+","0%2B").replace("&","%26").replace(" ","+")

def get_search_url(query):
	return "http://www.google.co.in/search?tbm=bks&hl=en&q=%s" % (normalize_query(query))

def get_html(url):
	try:
		#proxy = urllib2.ProxyHandler({'http':'http://f2010181:rzw20gf@10.1.9.36:8080'})
		#auth = urllib2.HTTPBasicAuthHandler()
		#opener = urllib2.build_opener(proxy, auth, urllib2.HTTPHandler)
		#urllib2.install_opener(opener)
		request = urllib2.Request(url)
		request.add_header("User-Agent","Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101")
		html = urllib2.urlopen(request).read()
		return html
	except:
		print "Error accessing: ", url
		return None

query = raw_input("Enter the query: ")
print '\n'
url = get_search_url(query)
html = get_html(url)
parser = etree.HTMLParser()
tree = etree.parse(StringIO.StringIO(html), parser)
soup = BeautifulSoup(html)
lis = soup.findAll("li", attrs = {"class" : "g"})
urls = []
for li in lis:
	a = li.find("a")
	u = a["href"].split('&')[0]
	urls.append(u)

browser = Browser('chrome')

for i in urls:
	print i
	html = get_html(i)
	parser = etree.HTMLParser()
	tree = etree.parse(StringIO.StringIO(html), parser)
	values = "//td[@class='metadata_value']/span[@dir='ltr']//text()"
	vals = tree.xpath(values)	
	isbn10 = []
	c = 1
	for i in vals:
		try:
			a = i.split(',')[0].strip()
			b = i.split(',')[1].strip()
		except IndexError:
			pass
		try:
			a = int(a)
			b = int(b)
			browser.visit("http://catalog.loc.gov/")
			browser.fill('Search_Arg',str(b))
			try:
				bt = browser.find_by_value('Search')
				bt.click()
				browser.select("RD","3")
				browser.find_by_name("SAVE")
				print "Found"
			except:
				print 'Not found on LOC :',b	
				c = c + 1

		except ValueError:
			pass
	if(c > 4):
		print 'Too many wrong results. Exiting !'
		break 
browser.quit()
