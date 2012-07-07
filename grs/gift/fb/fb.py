import facebook
import pprint

import falabella

def get_likes():

	access_token = "AAAAAAITEghMBACtyYyArm7TNZBQilpCWH42NPFpehZBOUfbZCLGWjzB84UT2KR51egyl8b9m8K6SsuVkOqIEPIaZBQ6VSSsjLWoaMZBGHaQZDZD"

	graph = facebook.GraphAPI(access_token)

	likes = graph.get_connections("me", "likes")

	pp = pprint.PrettyPrinter(indent=4)



	data = likes["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	

	return names

