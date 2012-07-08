import facebook
import sys

def get_friends(access_token, user):
	graph = facebook.GraphAPI(access_token)

	friends = graph.get_connections(user.username, "friends")
	data = friends["data"]
	data = data[:10]
	frs = []


	if len(data) > 0:		
		for fr in data:
			aux = {}
			aux = fr
			#aux["picture"] = graph.get_connections(fr["id"], "picture")["url"]
			aux["picture"] = ""
			frs.append(aux)

	return frs

def get_likes(access_token, id, limit=10):
	graph = facebook.GraphAPI(access_token)
	likes = graph.get_connections(id, "likes")
	data = likes["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	

	return names

def friend_likes(access_token, user):
	graph = facebook.GraphAPI(access_token)

	friends = get_friends(access_token, user)

	likes = {}
	for friend in friends:
		name = friend['name']
		f_id = friend['id']

		likes[f_id] = {
			'name': name,
			'likes': get_likes(access_token, f_id)
		}

	return likes