# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from fb.fb import get_likes


def index(request):
	return HttpResponse("buena cabros")
	#return render_to_response("index.kindle",{"variable":"hola"})


def fb(request):
	return HttpResponse(get_likes())

def templates(request):
	return render_to_response("index.kindle",{"variable":"hola"})

