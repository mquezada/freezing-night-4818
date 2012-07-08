from BeautifulSoup import BeautifulSoup
import mechanize

def feriamix(term):
	url = "http://www.feriamix.cl/cgi-bin/wspd_cgi.sh/WService=wsPFDD/inicio.p"

	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=1)
	b['busqueda'] = term

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('table', {'class' : 'filete_fichas_cd'})

	result = []
	for prod in prods:
		elem = prod.find('span', {'class' : 'txt_fichas_buscador'})

		tipo = elem.text
		artista = elem.next.next.text
		album = elem.next.next.next.next.next

		nombre = "%s - %s (%s)" % (artista, album, tipo)
		pelem = prod.find('span', {'class': 'txt_fichas_interiores_precio_inertet'})
		precio = pelem.text.split(' ')[1]

		link = pelem.find('a')['href']

		img = prod.find('img')['src']


		result.append({
			'nombre' : nombre,
		 	'link' : link,
		 	'img' : img,
		 	'precio' : precio,
		 	'desc' : ""
		 	})

	return result

def main():
	print feriamix("daddy yankee")

if __name__ == '__main__':
	main()