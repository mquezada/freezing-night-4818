
import mechanize

def falabella(term):

	url = "http://www.falabella.com/falabella-cl/"
	b = mechanize.Browser()
	b.set_handle_robots(False)

	b.open(url)
	b.select_form(nr=0)
	b['texto-busqueda'] = term

	return b.submit().read()