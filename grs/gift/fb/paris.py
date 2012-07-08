from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import mechanize

def paris(term):
	prefix = " http://www.paris.cl/webapp/wcs/stores/servlet/"
	imgprefix = "http://www.paris.cl"
	url = "http://www.paris.cl/webapp/wcs/stores/servlet/topcategory_10001_40000000577_-5_on"
 
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['buscador'] = smart_str(term)

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'class' : 'cat-term-caja-buscadorproducto'})

	result = []

	for prod in prods:

		nombre = prod.find('div', {'class' : 'descP2011'}).text
		link = prod.find('div', {'class' : 'descP2011'}).a['href']
		img = prod.find('div', {'class' : 'mrgnFt2'}).a.img['src']
		precio = prod.find('div', {'class' : 'prcIntB2011'})

		if precio is not None:
			precio = precio.text
		else:
			precio = ""

		result.append({
		 	'nombre' : nombre,
		 	'link' : "%s%s" % (prefix, link),
		 	'img' : "%s%s" % (imgprefix, img),
		 	'precio' : precio,
		 	'desc' : "",
			'likeAsociado': term
		 	})

	return result