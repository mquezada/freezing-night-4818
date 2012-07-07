from BeautifulSoup import BeautifulSoup
import mechanize

def paris(term):
	prefix = " http://www.paris.cl/webapp/wcs/stores/servlet/"
	imgprefix = "http://www.paris.cl"
	url = "http://www.paris.cl/webapp/wcs/stores/servlet/topcategory_10001_40000000577_-5_on"
 
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['buscador'] = term

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'class' : 'cat-term-caja-buscadorproducto'})

	result = []

	for prod in prods:
		print prod

		nombre = prod.find('div', {'class' : 'descP2011'}).text
		link = prod.find('div', {'class' : 'descP2011'}).a['href']
		img = prod.find('div', {'class' : 'mrgnFt2'}).a.img['src']
		precio = prod.find('div', {'class' : 'prcIntB2011'}).text

		result.append({
		 	'nombre' : nombre,
		 	'link' : "%s%s" % (prefix, link),
		 	'img' : "%s%s" % (imgprefix, img),
		 	'precio' : precio,
		 	'desc' : ""
		 	})

	return result

def main():
	print paris("iphone")


if __name__ == '__main__':
	main()