from BeautifulSoup import BeautifulSoup
import mechanize

def ripley(term):
	
	url = "http://www.ripley.cl/webapp/wcs/stores/servlet/StoreCatalogDisplay?storeId=10051&catalogId=10051"
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['q'] = term

	html = b.submit().read()

	soup = BeautifulSoup(html)
