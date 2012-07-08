from falabella import falabella
from paris import paris
from ebay import ebay
from feriamix import feriamix
from threading import Thread

class GiftSource(object):
	"""docstring for GiftSource"""
	def __init__(self, source, recommendations):
		super(GiftSource, self).__init__()
		self.source = source
		self.recommendations = recommendations
		
#t = Thread(target=self.search, args=(url, key_id))


recommendations = {}

def add_rec(name, method, term):
	global recommendations

	if not recommendations.has_key(name):
		recommendations[name] = []
	recommendations[name].extend(method(term))

def aggregate(terms):
	threads = []
	for term in terms:
		term_threads = [
			#Thread(target=add_rec, args=('Falabella', falabella, term)),
			Thread(target=add_rec, args=('Paris', paris, term)),
			#Thread(target=add_rec, args=('Ebay', ebay, term)),
			#Thread(target=add_rec, args=('Feriamix', feriamix, term))
		]

		map(lambda t : t.start(), term_threads)
		threads += term_threads

	map(lambda t : t.join(), threads)		
	
	return recommendations