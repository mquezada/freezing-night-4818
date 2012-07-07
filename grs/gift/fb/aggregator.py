from falabella import falabella
from paris import paris
from ebay import ebay


class GiftSource(object):
	"""docstring for GiftSource"""
	def __init__(self, source, recommendations):
		super(GiftSource, self).__init__()
		self.source = source
		self.recommendations = recommendations
		


def aggregate(terms):
	recommendations = {}

	for term in terms:
		sources = [
			GiftSource('Falabella', falabella(term)),
			GiftSource('Paris', paris(term)),
			GiftSource('Ebay', ebay(term))
		]		

		for s in sources:
			if not recommendations.has_key(s.source):
				recommendations[s.source] = []
			recommendations[s.source].extend(s.recommendations)
	
	return recommendations