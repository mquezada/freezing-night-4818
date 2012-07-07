import facebook
import pprint

import falabella

def get_likes():

	access_token = "AAAAAAITEghMBAJoZALDZCueviVZAIbfmgtHXIh3N8JZADksZA11WyZCXtBeZCZBBcUQ1fn5E9FT0ZAJgZCyIkFUE24tuTZB6z23YG2c3dDzGK2RLAZDZD"

	graph = facebook.GraphAPI(access_token)

	likes = graph.get_connections("me", "likes")

	pp = pprint.PrettyPrinter(indent=4)



	data = likes["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	

	return names

def main():
	print get_likes()

if __name__ == '__main__':
	main()