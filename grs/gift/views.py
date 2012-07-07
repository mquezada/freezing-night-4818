# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from fb.aggregator import aggregate


def index(request):
	return HttpResponse("buena cabros")
	#return render_to_response("index.kindle",{"variable":"hola"})


def fb(request):
	terms = ['iphone', 'harry potter', 'chocolate']

	return render_to_response("recommendations.html", {'items' : aggregate(terms)})

def templates(request):
	return render_to_response("index.kindle",{"variable":"hola"})

