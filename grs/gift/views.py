# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse

def index(request):
	return HttpResponse("buena cabros")
	#return render_to_response("index.kindle",{"variable":"hola"})

def templates(request):
	#return render_to_response("index.kindle",{"variable":"hola"})