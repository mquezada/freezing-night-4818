import urllib
import mechanize
import simplejson as json

def ebay(term):
	base_url = "http://svcs.sandbox.ebay.com/services/search/FindingService/v1?OPERATION-NAME=findItemsByKeywords&SERVICE-VERSION=1.11.0&SECURITY-APPNAME=Hashtag70-08b3-4798-b42e-243a5f7221d&RESPONSE-DATA-FORMAT=JSON&REST-PAYLOAD&paginationInput.entriesPerPage=10"

	query = urllib.quote(term)

	url = base_url + "&keywords=" + query

	b = mechanize.Browser()
	b.set_handle_robots(False)
	data = b.open(url).read()
	j = json.loads(data)

	hierba = j['findItemsByKeywordsResponse'][0]

	results = []

	if hierba['ack'][0] == 'Success':
		verde = hierba['searchResult'][0]
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
				'precio' : precio				
				})

	return results

def main():
	print ebay("iphone")

if __name__ == '__main__':
	main()






	