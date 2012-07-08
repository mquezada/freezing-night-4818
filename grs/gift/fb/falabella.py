from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import mechanize

def falabella(term):

	prefix = "http://www.falabella.com"
	url = "http://www.falabella.com/falabella-cl/"
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['texto-busqueda'] = smart_str(term)

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'class' : 'cajaLP4x'})

	result = []
	for prod in prods:
		 nombre = prod.find('div', {'class' : 'detalle'}).text
		 link = prod.find('div', {'class' : 'detalle'}).a['href']
		 img = prod.find('div', {'class' : 'quickView'}).a.img['src']
		 precio1 = prod.find('div', {'class' : 'precio1'}).text

		 result.append({
		 	'nombre' : nombre,
		 	'link' : "%s%s" % (prefix, link),
		 	'img' : img,
		 	'precio' : precio1,
		 	'desc' : ""
		 	})

	return result