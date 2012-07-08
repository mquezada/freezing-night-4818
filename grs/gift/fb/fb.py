import facebook
import sys
import locale
from datetime import *

def get_friends(access_token, user, limit=10):
	graph = facebook.GraphAPI(access_token)

	friends = graph.get_connections(user.username, "friends", fields=['name','birthday','picture'])
	data = friends["data"]
	map(format_fecha, data)
	data.sort(cmp_dates)
	if limit != 0:
		data = data[:limit]
	frs = []


	if len(data) > 0:		
		for fr in data:
			frs.append(fr)

	return frs

def get_likes(access_token, id, limit=5):

	graph = facebook.GraphAPI(access_token)
	likes = graph.get_connections(id, "likes")
	data = likes["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	
			
	return data[:limit]

def get(access_token, id, term, limit=20):
	graph = facebook.GraphAPI(access_token)
	cosas = graph.get_connections(id, term)
	data = cosas["data"]
	names = []

	if len(data) > 0:
		for like in data:
			names.append(like["name"])	
			
	return data[:limit]

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

def get_likes_likes(access_token, id):
	graph = facebook.GraphAPI(access_token)
	info = graph.get_object(id)

	return info

def cmp_dates(f1,f2):
	if "birthday" not in f1:
		return 1
	if "birthday" not in f2:
		return -1

	b1 = datetime.strptime(f1["birthday2"], "%m/%d")
	b2 = datetime.strptime(f2["birthday2"], "%m/%d")
	today = datetime.today()

	#ejemplo. b1 en enero, b2 en febrero, actual marzo, mas cercano b1
	if today.month > b1.month and today.month > b2.month:
		if b1.month < b2.month:
			return -1
		elif b1.month > b2.month:
			return 1
		else:
			if b1.day < b2.day:
				return -1
			else:
				return 1

	#ejemplo b1 en entero, actual febrero, b2 marzo
	if b1.month < today.month and today.month < b2.month:
		return 1
	#ejemplo b2 en entero, actual febrero, b1 marzo
	if b2.month < today.month and today.month < b1.month:
		return -1

	#ejemplo. actual enero, b1 en febrero, b2 en marzo
	if today.month < b1.month and today.month < b2.month:
		if b1.month < b2.month:
			return -1
		elif b1.month > b2.month:
			return 1
		else:
			if b1.day < b2.day:
				return -1
			else:
				return 1

	#mes de b1, b2 y actual el mismo
	if today.month == b1.month and today.month == b2.month:
		#b1 y b2 mayores en dias
		if today.day < b1.day and today.day < b2.day:
			return cmp(b1.day,b2.day)
		#b1 y b2 menores
		if today.day > b1.day and today.day > b2.day:
			return cmp(b1.day,b2.day)
		if today.day > b1.day:
			return -1
		if today.day > b2.day:
			return 1


	#mes de b1 es igual a actual
	if today.month == b1.month:
		if today.day < b1.day:
			return -1
		else:
			return 1
	#mes de b1 es igual a actual
	if today.month == b2.month:
		if today.day < b2.day:
			return 1
		else:
			return -1


	return cmp(b1,b2)

def format_fecha(data):
	if "birthday" in data:
		b1list = data["birthday"].split("/")
		b1 = b1list[0]+"/"+b1list[1]
		data["birthday2"] = b1
		aux = datetime.strptime(b1, "%m/%d")
		data["birthdayString"] = datetime.strftime(aux, "%B %d")
