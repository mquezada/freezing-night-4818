from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import mechanize

def zmart(term):

	prefix = "http://www.zmart.cl"
	url = "http://www.zmart.cl/Scripts/default.asp"

	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['strSearch'] = smart_str(term)

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'id' : 'busqueda'})[0].findAll('div', {'class': 'caja_minihome'})

	result = []
	for prod in prods:
		 nombre = prod.h3.text
		 link = prod.h3.a['href']
		 img = prod.img['src']
		 precio1 = prod.li.next.next.next.text

		 result.append({
		 	'nombre' : nombre,
		 	'link' : "%s%s" % (prefix, link),
		 	'img' : "%s%s" % (prefix, img),
		 	'precio' : precio1,
		 	'desc' : "",
			'likeAsociado': term
		 	})

	return result


def main():
	print zmart('final fantasy')


if __name__ == '__main__':
	main()