# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from fb.aggregator import aggregate
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from social_auth.models import *
from fb.fb import *
import facebook
import operator
from threading import Thread

def index(request):
	params = {"user": None}
	if "user" in request.session:
		return redirect("/logged")

	return render_to_response("index.html",params)

def templates(request):
	return render_to_response("index.kindle",{"variable":"hola"}, context_instance=RequestContext(request))
	
	username = ''
	if "user" in request.session:
		username = request.session['user']
	
	return render_to_response("index.kindle",{"variable":"hola", "username":username}, context_instance=RequestContext(request))


def fb(request):
	terms = ['iphone', 'harry potter', 'chocolate']
	user = request.user
	
	print user
	access_token = UserSocialAuth.objects.get(user_id=user.id).extra_data['access_token']

	print get_likes(access_token, user)
	return render_to_response("recommendations.html", {'items' : aggregate(terms)})

def logged(request):
	request.session["user"] = request.user
	request.session["access_token"] = UserSocialAuth.objects.get(user_id=request.user.id).extra_data['access_token']
	graph = facebook.GraphAPI(request.session["access_token"])
	request.session["picture"] = graph.get_connections(request.user.username, "picture")["url"]
	return redirect("/friends")

	
def friends(request):
	if "user" not in request.session or "access_token" not in request.session:
		return redirect("/")

	user = request.session["user"]
	picture = request.session["picture"]
	access_token = request.session["access_token"]
	

	#print friend_likes(access_token, user)

	allFriends = get_friends(access_token, user, 0)
	friends = allFriends[:10]
	allFriends = map(lambda x: x["name"], allFriends)
	return render_to_response("friends.html", {"user":user, "friends":friends, "picture": picture, "allFriends": allFriends}, context_instance=RequestContext(request))

	#return render_to_response("logged.kindle",{"access_token":access_token, "username":user.username}, context_instance=RequestContext(request))

def search(request):
	name = request.POST["buscar"]
	friends = get_friends(request.session["access_token"], request.session["user"], 0)
	for friend in friends:
		if friend["name"]==name:
			return redirect("/friends_likes/"+str(friend["id"]))

def friendsLikes(request, id=-1):
	if id == -1:
		return redirect("/")

	likes = get_likes(request.session["access_token"], id)
	tieneLikes = True
	if len(likes) == 0:
		tieneLikes = False

	recommendations = aggregate('music', likes)
	
	return render_to_response(
		"friendsLikes.html", 
		{"likes":likes, "recommendations":recommendations, "tieneLikes":tieneLikes},
		context_instance=RequestContext(request))

def aggregate_wrapper(name, l, result):
	result.update(aggregate(name, l))

def get_wrapper(token, id, name, result):
	result.extend(get(token, id, name))


def recommendations(request, id=-1):
	if id < 0:
		return redirect("/")

	books = []
	games = []
	music = []
	movies = []

	threads = [
		Thread(target=get_wrapper, args=(request.session['access_token'], id, 'books', books)),
		Thread(target=get_wrapper, args=(request.session['access_token'], id, 'games', games)),
		Thread(target=get_wrapper, args=(request.session['access_token'], id, 'music', music)),
		Thread(target=get_wrapper, args=(request.session['access_token'], id, 'movies', movies))
	]

	map(lambda t : t.start(), threads)
	map(lambda t : t.join(), threads)

	rbooks = {}
	rgames = {}
	rmusic = {}
	rmovies = {}

	threads = [
		Thread(target=aggregate_wrapper, args=('books', books, rbooks)),
		Thread(target=aggregate_wrapper, args=('music', music, rmusic)),
		Thread(target=aggregate_wrapper, args=('games', games, rgames)),
		Thread(target=aggregate_wrapper, args=('movies', movies, rmovies)),
	]

	map(lambda t : t.start(), threads)
	map(lambda t : t.join(), threads)

	print rmusic
	
	recs = dict(rbooks.items() + rmusic.items() + rmovies.items() + rgames.items())

	if len(recs) > 0:
		tieneLikes = True
	else:
		tieneLikes = False

	return render_to_response("friendsLikes.html", {'recommendations' : recs, 'tieneLikes' : tieneLikes}) 

def logout(request):
	if "user" in request.session:
		del request.session["user"]
	return redirect("/")


def c(request, id=-1):
	likes = get_likes(request.session["access_token"], id)
	categories = {}
	for like in likes:
		if like["category"] in categories:
			categories[like["category"]] += 1
		else:
			categories[like["category"]]  = 1
		print get_likes_likes(request.session["access_token"],like["id"])
	
	categories = sorted(categories.iteritems(), key=operator.itemgetter(1))
	categories.reverse()

	return render_to_response("c.html", {"likes":likes, "categories":categories}, context_instance=RequestContext(request))
