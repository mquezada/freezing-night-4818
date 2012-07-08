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
	print picture
	access_token = request.session["access_token"]
	

	#print friend_likes(access_token, user)
	friends = get_friends(access_token, user)
	friends = friends[:10]
	return render_to_response("friends.html", {"user":user, "friends":friends, "picture": picture}, context_instance=RequestContext(request))

	#return render_to_response("logged.kindle",{"access_token":access_token, "username":user.username}, context_instance=RequestContext(request))

def friendsLikes(request, id=-1):
	if id == -1:
		return redirect("/")

	likes = get_likes(request.session["access_token"], id)
	print likes
	return render_to_response("friendsLikes.html", {"likes":likes},context_instance=RequestContext(request))


def logout(request):
	if "user" in request.session:
		del request.session["user"]
	return redirect("/")
