from falabella import falabella
from paris import paris
from ebay import ebay2
from feriamix import feriamix
from books.buscalibros import buscalibros
from music.mercadolibre import mercadolibre
from games.zmart import zmart

class GiftSource(object):
	"""docstring for GiftSource"""
	def __init__(self, source, recommendations):
		super(GiftSource, self).__init__()
		self.source = source
		self.recommendations = recommendations


def aggregate(category, terms):
	recommendations = {}
	for term in terms:
		term = term["name"]

		if not recommendations.has_key(category):
			recommendations[category] = []

		if category == 'movies':
			recommendations['movies'].extend(ebay2(term, 'movies'))			
			recommendations['movies'].extend(mercadolibre(term, 'peliculas'))

		elif category == 'music':
			recommendations['music'].extend(ebay2(term, 'music'))
			#recommendations['music'].extend(mercadolibre(term, 'musica'))

		elif category == 'books':
			recommendations['books'].extend(buscalibros(term))

		elif category == 'games':
			recommendations['games'].extend(zmart(term))
			recommendations['games'].extend(mercadolibre(term, 'juegos'))
	
	
	return recommendations