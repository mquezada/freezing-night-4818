import urllib
import mechanize
from django.utils.encoding import smart_str, smart_unicode
import simplejson as json

categories = {
	'music' : '11233',
	'movies' : '11232',
	'games' : '1249',
	'books' : '267'
}

def get_category(category):
	return categories[category]

def by_category(term, id):	
	base_url = "http://svcs.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsAdvanced&SERVICE-VERSION=1.11.0&SECURITY-APPNAME=Hashtag13-5eca-4bcf-8db6-24321011273&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=10&keywords=%s&categoryId=%s&descriptionSearch=false&outputSelector=GalleryInfo"

	query = urllib.quote(smart_str("\"%s\"" % term))
	url = base_url % (query, id)

	return url


def ebay2(term, category):
	url = by_category(term, get_category(category))
	b = mechanize.Browser()
	b.set_handle_robots(False)
	data = b.open(url).read()
	j = json.loads(data)

	hierba = j['findItemsAdvancedResponse'][0]

	results = []

	if hierba['ack'][0] == 'Success':
		verde = hierba['searchResult'][0]

		if not verde['@count'] == '0':
			for item in verde['item']:
				nombre = item['title'][0]
				link = item['viewItemURL'][0]
				if item.has_key('galleryURL'):
					img = item['galleryURL'][0]
				else:
					img = "http://www.buscalibros.cl/imagenes/no-imagen-chica.gif"
				desc = ""
				precio = "%s %s" % (item['sellingStatus'][0]['convertedCurrentPrice'][0]['@currencyId'], item['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__'])
		
				results.append({
					'nombre' : nombre,
					'link' : link,
					'img' : img,
					'desc' : desc,
					'precio' : precio,
					'likeAsociado': term
					})

	return results

def ebay(term):
	base_url = "http://svcs.sandbox.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.11.0&SECURITY-APPNAME=Hashtag70-08b3-4798-b42e-243a5f7221d&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=10"

	query = urllib.quote(smart_str(term))

	url = base_url + "&keywords=" + query

	b = mechanize.Browser()
	b.set_handle_robots(False)
	data = b.open(url).read()
	j = json.loads(data)

	hierba = j['findItemsByKeywordsResponse'][0]

	results = []

	if hierba['ack'][0] == 'Success':
		verde = hierba['searchResult'][0]

		if not verde['@count'] == '0':
			for item in verde['item']:
				nombre = item['title'][0]
				link = item['viewItemURL'][0]
				img = ""
				desc = ""
				precio = "%s %s" % (item['sellingStatus'][0]['convertedCurrentPrice'][0]['@currencyId'], item['sellingStatus'][0]['convertedCurrentPrice'][0]['__value__'])
		
				results.append({
					'nombre' : nombre,
					'link' : link,
					'img' : img,
					'desc' : desc,
					'precio' : precio,
					'likeAsociado': term
					})

	return results





	