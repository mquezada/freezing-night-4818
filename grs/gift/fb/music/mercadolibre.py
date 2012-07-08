import simplejson as json

from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import urllib
import mechanize

def mercadolibre(term, cat):
	prefix = "http://www.buscalibros.cl/"
	url = "https://api.mercadolibre.com/sites/MLC/search?limit=10&q=%s&category=%s"

	url = url % (urllib.quote("\"%s\"" % smart_str(term)), cat)

	b = mechanize.Browser()
	b.set_handle_robots(False)
	
	html = b.open(url).read()

	soup = BeautifulSoup(html)

	data = json.loads(str(soup))

	result = []

	for prod in data['results']:
		nombre = prod['title']
		link = prod['permalink']
		img = prod['thumbnail']
		precio = "$ %d" % prod['price']

		result.append({
		 	'nombre' : nombre,
		 	'link' : link,
		 	'img' : img,
		 	'precio' : precio,
		 	'desc' : "",
			'likeAsociado': term
		 	})

	g_results = []

	for r in result:
		if term.lower() in r['nombre'].lower():
			g_results.append(r)


	return g_results


def main():
	print mercadolibre("daddy yankee")

if __name__ == '__main__':
	main()