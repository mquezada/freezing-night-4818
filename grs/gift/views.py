# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from fb.aggregator import aggregate
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from django.template import RequestContext
from social_auth.models import *
from fb.fb import get_likes

def index(request):
	return HttpResponse("buena cabros")
	#return render_to_response("index.kindle",{"variable":"hola"})

def templates(request):
	return render_to_response("index.kindle",{"variable":"hola"}, context_instance=RequestContext(request))
	



def fb(request):
	terms = ['iphone', 'harry potter', 'chocolate']
	user = request.user
	
	print user
	access_token = UserSocialAuth.objects.get(user_id=user.id).extra_data['access_token']




	print get_likes(access_token, user)

	return render_to_response("recommendations.html", {'items' : aggregate(terms)})

def logged(request):
	user = request.user
	access_token = UserSocialAuth.objects.get(user_id=user.id).extra_data['access_token']
	return render_to_response("logged.kindle",{"access_token":access_token, "username":user.username}, context_instance=RequestContext(request))

