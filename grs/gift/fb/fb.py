import facebook
import pprint

import falabella

def get_likes(access_token, user):
	graph = facebook.GraphAPI(access_token)

	likes = graph.get_connections(user.id, "likes")
	pp = pprint.PrettyPrinter(indent=4)
	data = likes["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	

	return names