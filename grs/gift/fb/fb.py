import facebook

def get_friends(access_token, user, limit=5):
	graph = facebook.GraphAPI(access_token)

	friends = graph.get_connections(user.username, "friends")

	data = friends["data"]
	names = []

	i = 1
	if len(data) > 0:
		for fr in data:
			names.append(fr)
			if i == limit:
				break
			i += 1

	return names

def get_likes(access_token, id, limit=10):
	graph = facebook.GraphAPI(access_token)

	likes = graph.get_connections(id, "likes")

	data = likes["data"]
	names = []

	i = 1
	if len(data) > 0:
		for like in data:
			names.append(like["name"])	
			if i == limit:
				break
			i += 1

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