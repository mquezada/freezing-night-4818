from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import urllib
import mechanize

def buscalibros(term):
	prefix = "http://www.buscalibros.cl/"
	url = "http://www.buscalibros.cl/buscar.php?tipo_busqueda=todos&titulo=%s&autor=&x=0&y=0"

	url = url % (urllib.quote(smart_str(term)))

	b = mechanize.Browser()
	b.set_handle_robots(False)
	
	html = b.open(url).read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'id' : 'box_categoria'})

	result = []

	for prod in prods:
		nombre = prod.table.h4.text
		link = prod.table.h4.a['href']		
		img = prod.table.img['src']
		precio = prod.find('span', {'class':'precio_rojo'})

		if precio is not None:
			precio = precio.text
		else:
			precio = "Precio no disponible"

		result.append({
		 	'nombre' : nombre,
		 	'link' : "%s%s" % (prefix, link),
		 	'img' : "%s%s" % (prefix, img),
		 	'precio' : precio,
		 	'desc' : "",
			'likeAsociado': term
		 	})

	return result


def main():
	print buscalibros("quijote de la mancha")

if __name__ == '__main__':
	main()