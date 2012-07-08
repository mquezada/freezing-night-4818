from BeautifulSoup import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import mechanize

def blockbuster(term):

	prefix = "http://www.blockbuster.cl/default.aspx"
	url = "http://www.blockbuster.cl/default.aspx"
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['ctl00$txtBuscar'] = smart_str(term)

	html = b.submit().read()

	soup = BeautifulSoup(html)

	prods = soup('div', {'id' : 'ctl00_ContentPlaceHolder1_DataList1'})

	print prods
	pass

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
		 	'desc' : "",
			'likeAsociado': term
		 	})

	return result


def main():
	print blockbuster('avengers')


if __name__ == '__main__':
	main()