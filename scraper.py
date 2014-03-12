from BeautifulSoup import BeautifulSoup
import urllib2, StringIO, sys
from lxml import etree
from sys import exit


def normalize_query(query):
	return query.strip().replace(":","%3A").replace("+","0%2B").replace("&","%26").replace(" ","+")

def get_search_url(query, page = 0, per_page = 10):
	return "http://www.google.com/search?hl=en&q=%s&start=%i&num=%i" % (normalize_query(query), page * per_page, per_page)

def get_html(url):
	try:
		request = urllib2.Request(url)
		request.add_header("User-Agent","Mozilla/5.001 (windows; U; NT4.0; en-US; rv:1.0) Gecko/25250101")
		html = urllib2.urlopen(request).read()
		return html
	except:
		print "Error accessing: ", url
		return None

class GoogleResult:
	def __init__(self):
		self.name = None
		self.link = None
		self.description = None
		self.page = None
		self.index = None

class Google:
	@staticmethod
	def search(query, pages=1):
		results = []
		for i in range(pages):
			url = get_search_url(query, i)
			html = get_html(url)
			if html:
				soup = BeautifulSoup(html)
				lis = soup.findAll("li", attrs = {"class" : "g"})
				j = 0
				for li in lis:
					res = GoogleResult()
					res.page = i
					res.index = j
					a = li.find("a")
					res.name = a.text.strip()
					res.link = a["href"]
					res.link = res.link.split('&sa')[0]
					res.link = res.link.split('q=')[1]					
					if res.link.startswith("/search?"):
						continue
					sdiv = li.find("div", attrs = {"class" : "s"})
					if sdiv:
						res.description = sdiv.text.strip()
					results.append(res)
					j = j + 1
		return results	


def test(query, num):
	flag = {'amz':0,'flp':0,'goog':0}
	search = Google.search(query, num)
	for i in search:
		if 'books.google' in i.link:
			google_books_url = i.link
			flag['goog'] = 1
		if 'amazon' in i.link:
			amz_url = i.link
			flag['amz'] = 1
		if i.link.find('http://www.flipkart') != -1:
			flp_url = i.link
			flag['flp'] = 1

		print i.name,'\n',i.link,'\n'

	if search is None or len(search) == 0:
		print "ERROR: No resuts"
	else:
		print "PASSED: {0} Search Reuslts\n".format(len(search))

	if flag['flp'] == 1:
		try:
			html = get_html(flp_url)
			parser = etree.HTMLParser()
			tree = etree.parse(StringIO.StringIO(html), parser)
			fields = tree.xpath("//td[@class='specs-key']/text()")
			values = tree.xpath("//td[@class='specs-value fk-data']/text()")
			print "---From Flipkart---\n"
			for i in range(len(values)):
				print fields[i].strip(),':			',values[i].strip()
			exit(0)
		except:
			pass

	elif flag['amz'] == 1:
		try:		
			amz_url = amz_url.replace("%3F","?").replace("%3D","=")
			html = get_html(amz_url)
			parser = etree.HTMLParser()
			tree = etree.parse(StringIO.StringIO(html), parser)

			
			count = tree.xpath("count(//div[@class='content']/ul/li/b)")
			authour = tree.xpath("//span[@class='contributorNameTrigger']//text()")
			category = tree.xpath("//option[@value='search-alias=stripbooks']/text()")
			title = tree.xpath("//span[@id='btAsinTitle']/text()")

			field_val = "//td[@class='bucket']/div/ul/li[%d]//text()"
			print 'Title 		: ',title[0]

			if count < 5:
				print "Can't extract exact results !"
			print '---From Amazon---\n'
			for i in range(1,6,1):
				val = tree.xpath(field_val%(i))
				print val[0].rstrip(':'),'	:',val[1]

			print 'Authour		: ',authour
			sys.exit()
		except:
			pass
			

	elif flag['goog'] == 1:
		try:		
			google_books_url = google_books_url.replace("%3F","?").replace("%3D","=")
			html = get_html(google_books_url)

			parser = etree.HTMLParser()
			tree = etree.parse(StringIO.StringIO(html), parser)

			values = "//td[@class='metadata_value']/span[@dir='ltr']//text()"
			fields = "//td[@class='metadata_label']//text()"
			authour = tree.xpath("//tr[2]/td[@class='metadata_value']//span/text()")

			vals = tree.xpath(values)
			vals.insert(1, authour[0])
			attrs = tree.xpath(fields)

			length = min(len(vals), len(attrs))
			print '---From google-books---\n'
			for i in range(length):
				print attrs[i]+'	:'+vals[i]
		except:
			print 'Improve your query !!'

def main():
	query = raw_input("Enter the query: ")
	num = raw_input("Enter the number of pages of results:")
	print '\n'
	test(query, int(num))

if __name__ == '__main__':
	main()
