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
	m_user = dir(request.user)
	request.session["access_token"] = UserSocialAuth.objects.get(user_id=request.user.id).extra_data['access_token']
	graph = facebook.GraphAPI(request.session["access_token"])
	request.session["picture"] = graph.get_connections(request.user.username, "picture")['url']

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
			return redirect("/recommendations/"+str(friend["id"]))

def friendsLikes(request, id=-1):
	if id == -1:
		return redirect("/")

	likes = get_likes(request.session["access_token"], id)
	print id
	tieneLikes = True

	#recommendations = {'Ebay': [{'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 16.35', 'link': u'http://cgi.sandbox.ebay.com/All-Volcanoes-/110100520346?pt=LH_DefaultDomain_0', 'nombre': u'All About Volcanoes', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 0.99', 'link': u'http://cgi.sandbox.ebay.com/STORIES-ALL-/110100460745?pt=US_Childrens_Books', 'nombre': u'STORIES FOR ALL', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 14.95', 'link': u'http://cgi.sandbox.ebay.com/GroVia-Newborn-All-One-Cloth-Diaper-Mod-Flower-/110100512426?pt=LH_DefaultDomain_0', 'nombre': u'GroVia Newborn All in One Cloth Diaper - Mod Flower', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 7.88', 'link': u'http://cgi.sandbox.ebay.com/Ty-Pluffies-Snoopy-All-Blue-/110100480646?pt=LH_DefaultDomain_0', 'nombre': u'Ty Pluffies Snoopy - All Blue', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 6.59', 'link': u'http://cgi.sandbox.ebay.com/Bumkins-Waterproof-Super-Bib-All-Star-/110100510690?pt=LH_DefaultDomain_0', 'nombre': u'Bumkins Waterproof Super Bib, All Star', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 15.0', 'link': u'http://cgi.sandbox.ebay.com/MD-MOMS-Baby-Silk-Grentle-All-Over-Clean-Hair-and-Body-Wash-/110100515652?pt=LH_DefaultDomain_0', 'nombre': u'MD MOMS Baby Silk Grentle All Over Clean Hair and Body Wash', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 8.4', 'link': u'http://cgi.sandbox.ebay.com/Mod-Podge-Gloss-All-In-One-Decoupage-Sealer-Glue-Finish-4-fl-oz-/110100518030?pt=LH_DefaultDomain_0', 'nombre': u'Mod Podge Gloss All-In-One Decoupage Sealer / Glue / Finish (4 fl. oz. )', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 9.25', 'link': u'http://cgi.sandbox.ebay.com/Dance-All-Night-Magnetic-Tin-Dress-Up-Set-/110100478852?pt=LH_DefaultDomain_0', 'nombre': u'Dance All Night Magnetic Tin Dress-Up Set', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 12.98', 'link': u'http://cgi.sandbox.ebay.com/Star-Wars-Head-Shape-Carry-All-Tin-Box-Styles-may-vary-one-piece-/110100516383?pt=LH_DefaultDomain_0', 'nombre': u'Star Wars Head Shape Carry All Tin Box Styles may vary (one piece)', 'desc': ''}, {'img': '', 'likeAsociado': u'ALL', 'precio': u'USD 17.77', 'link': u'http://cgi.sandbox.ebay.com/Ty-Beanie-Buddy-Hello-Kitty-All-Pink-Large-/110100480932?pt=LH_DefaultDomain_0', 'nombre': u'Ty Beanie Buddy Hello Kitty - All Pink (Large)', 'desc': ''}], 'Falabella': [{'img': u'http://falabella.scene7.com/is/image/Falabella/2977876?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$7.990', 'link': u'http://www.falabella.com/falabella-cl/product/2977876/Aventuras-en-el-parque?skuId=&passedNavAction=', 'nombre': u'Aventuras en el parque', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865047?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$7.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865047/Mama-Bee-Aceite-para-el-cuerpo-115-ml?skuId=&passedNavAction=', 'nombre': u'Mama Bee Aceite para el cuerpo 115...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3182707?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/3182707/Crema-Facial-dia-con-Aceite-de-Emu-55-gr?skuId=&passedNavAction=', 'nombre': u'Crema Facial d\xeda con Aceite de Em\xfa...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865505?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865505/Balsamo-para-el-vientre-de-Embarazada?skuId=&passedNavAction=', 'nombre': u'B\xe1lsamo para el vientre de Embaraz...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/prod680028?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/prod680028/Frazada-Polar-+-Cojin-Relleno?skuId=&passedNavAction=', 'nombre': u'Frazada Polar + Coj\xedn Relleno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3003920?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3003920/El-Picnic-de-Winnie?skuId=&passedNavAction=', 'nombre': u'El Picnic de Winnie', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3383081?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3383081/Cargador-USB-CP-ELS?skuId=&passedNavAction=', 'nombre': u'Cargador USB CP-ELS', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3324204?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3324204/Alisador-Midi-Travel?skuId=&passedNavAction=', 'nombre': u'Alisador Midi Travel', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2683098?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/2683098/Alisador-Handy?skuId=&passedNavAction=', 'nombre': u'Alisador Handy', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3068490?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$11.990', 'link': u'http://www.falabella.com/falabella-cl/product/3068490/Maquina-de-Hilos-para-el-Cabello?skuId=&passedNavAction=', 'nombre': u'Maquina de Hilos para el Cabello', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370780?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370780/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-chocolate?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370779?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370779/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-Beige?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2551600?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2551600/Golden-Line-Pen-Set?skuId=&passedNavAction=', 'nombre': u'Golden Line Pen Set', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3004893?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3004893/Prepara-y-sirva-el-desayuno-?skuId=&passedNavAction=', 'nombre': u'Prepara y sirva el desayuno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2388888?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2388888/Juego-Clue-Reinvencion-Quien-Es-el-Culpable?skuId=&passedNavAction=', 'nombre': u'Juego Clue Reinvenci\xf3n Qui\xe9n Es el...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2708416?$lista160$', 'likeAsociado': u'El Mostrador', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2708416/Alisador-Hp-8310?skuId=&passedNavAction=', 'nombre': u'Alisador Hp 8310', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3029656?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$3.990', 'link': u'http://www.falabella.com/falabella-cl/product/3029656/Pelotas-All-Court-French-Open-3-Unidades?skuId=&passedNavAction=', 'nombre': u'Pelotas All Court French Open 3 Un...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3029658?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$5.990', 'link': u'http://www.falabella.com/falabella-cl/product/3029658/Pelotas-All-Court-French-Open-4-Unidades?skuId=&passedNavAction=', 'nombre': u'Pelotas All Court French Open 4 Un...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3367654?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$14.990', 'link': u'http://www.falabella.com/falabella-cl/product/3367654/Juego-Sonic-&-Sega-All-Star-Racing?skuId=&passedNavAction=', 'nombre': u'Juego Sonic & Sega All Star Racing', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3367653?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$14.990', 'link': u'http://www.falabella.com/falabella-cl/product/3367653/Juego-Sonic-&-Sega-All-Star-Racing?skuId=&passedNavAction=', 'nombre': u'Juego Sonic & Sega All Star Racing', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2799544?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$19.900', 'link': u'http://www.falabella.com/falabella-cl/product/2799544/Exfoliante-Rostro-75-ml?skuId=&passedNavAction=', 'nombre': u'Exfoliante Rostro 75 ml', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3266724?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$19.990', 'link': u'http://www.falabella.com/falabella-cl/product/3266724/Zapatilla-Mujer-All-Star-Light?skuId=&passedNavAction=', 'nombre': u'Zapatilla Mujer All Star Light', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3264902?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$19.990', 'link': u'http://www.falabella.com/falabella-cl/product/3264902/Zapatilla-Mujer-Chuck-Taylor-All-Star?skuId=&passedNavAction=', 'nombre': u'Zapatilla Mujer Chuck Taylor All S...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/66963?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$21.400', 'link': u'http://www.falabella.com/falabella-cl/product/66963/Locion-Hidratante-y-Renovadora-de-Labios-12-ml?skuId=&passedNavAction=', 'nombre': u'Loci\xf3n Hidratante y Renovadora de ...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3159211?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$24.900', 'link': u'http://www.falabella.com/falabella-cl/product/3159211/Cardigan-All?skuId=&passedNavAction=', 'nombre': u'C\xe1rdigan All', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/68127?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$26.990', 'link': u'http://www.falabella.com/falabella-cl/product/68127/All-Mascaras-125-ml?skuId=&passedNavAction=', 'nombre': u'All Mascaras 125 ml', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/1050575?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$27.990', 'link': u'http://www.falabella.com/falabella-cl/product/1050575/Zapatilla-Hombre-All-Star-Season?skuId=&passedNavAction=', 'nombre': u'Zapatilla Hombre All Star Season', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3138207?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$27.990', 'link': u'http://www.falabella.com/falabella-cl/product/3138207/Zapatilla-Hombre-Chuck-Taylor-All-Star?skuId=&passedNavAction=', 'nombre': u'Zapatilla Hombre Chuck Taylor All ...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3158966?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$29.900', 'link': u'http://www.falabella.com/falabella-cl/product/3158966/Jersey-All-S?skuId=&passedNavAction=', 'nombre': u'Jersey All-S', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/prod560100?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$29.900', 'link': u'http://www.falabella.com/falabella-cl/product/prod560100/Jersey-All-S?skuId=&passedNavAction=', 'nombre': u'Jersey All-S', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/279857?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$29.900', 'link': u'http://www.falabella.com/falabella-cl/product/279857/Gel-Crema-Hidratante-Contorno-Ojos-15-ml?skuId=&passedNavAction=', 'nombre': u'Gel Crema Hidratante Contorno Ojos...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3119399?$lista160$', 'likeAsociado': u'ALL', 'precio': u'$39.990', 'link': u'http://www.falabella.com/falabella-cl/product/3119399/Zapatilla-Mujer-Chuck-Taylor-All-Star-Leather?skuId=&passedNavAction=', 'nombre': u'Zapatilla Mujer Chuck Taylor All S...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2977876?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$7.990', 'link': u'http://www.falabella.com/falabella-cl/product/2977876/Aventuras-en-el-parque?skuId=&passedNavAction=', 'nombre': u'Aventuras en el parque', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865047?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$7.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865047/Mama-Bee-Aceite-para-el-cuerpo-115-ml?skuId=&passedNavAction=', 'nombre': u'Mama Bee Aceite para el cuerpo 115...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3182707?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/3182707/Crema-Facial-dia-con-Aceite-de-Emu-55-gr?skuId=&passedNavAction=', 'nombre': u'Crema Facial d\xeda con Aceite de Em\xfa...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865505?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865505/Balsamo-para-el-vientre-de-Embarazada?skuId=&passedNavAction=', 'nombre': u'B\xe1lsamo para el vientre de Embaraz...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/prod680028?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/prod680028/Frazada-Polar-+-Cojin-Relleno?skuId=&passedNavAction=', 'nombre': u'Frazada Polar + Coj\xedn Relleno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3003920?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3003920/El-Picnic-de-Winnie?skuId=&passedNavAction=', 'nombre': u'El Picnic de Winnie', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3383081?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3383081/Cargador-USB-CP-ELS?skuId=&passedNavAction=', 'nombre': u'Cargador USB CP-ELS', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3324204?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3324204/Alisador-Midi-Travel?skuId=&passedNavAction=', 'nombre': u'Alisador Midi Travel', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2683098?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/2683098/Alisador-Handy?skuId=&passedNavAction=', 'nombre': u'Alisador Handy', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3068490?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$11.990', 'link': u'http://www.falabella.com/falabella-cl/product/3068490/Maquina-de-Hilos-para-el-Cabello?skuId=&passedNavAction=', 'nombre': u'Maquina de Hilos para el Cabello', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370780?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370780/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-chocolate?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370779?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370779/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-Beige?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2551600?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2551600/Golden-Line-Pen-Set?skuId=&passedNavAction=', 'nombre': u'Golden Line Pen Set', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3004893?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3004893/Prepara-y-sirva-el-desayuno-?skuId=&passedNavAction=', 'nombre': u'Prepara y sirva el desayuno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2388888?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2388888/Juego-Clue-Reinvencion-Quien-Es-el-Culpable?skuId=&passedNavAction=', 'nombre': u'Juego Clue Reinvenci\xf3n Qui\xe9n Es el...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2708416?$lista160$', 'likeAsociado': u'El Chavo', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2708416/Alisador-Hp-8310?skuId=&passedNavAction=', 'nombre': u'Alisador Hp 8310', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865047?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$7.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865047/Mama-Bee-Aceite-para-el-cuerpo-115-ml?skuId=&passedNavAction=', 'nombre': u'Mama Bee Aceite para el cuerpo 115...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2865505?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/2865505/Balsamo-para-el-vientre-de-Embarazada?skuId=&passedNavAction=', 'nombre': u'B\xe1lsamo para el vientre de Embaraz...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3182707?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$8.990', 'link': u'http://www.falabella.com/falabella-cl/product/3182707/Crema-Facial-dia-con-Aceite-de-Emu-55-gr?skuId=&passedNavAction=', 'nombre': u'Crema Facial d\xeda con Aceite de Em\xfa...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3003920?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3003920/El-Picnic-de-Winnie?skuId=&passedNavAction=', 'nombre': u'El Picnic de Winnie', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/prod680028?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/prod680028/Frazada-Polar-+-Cojin-Relleno?skuId=&passedNavAction=', 'nombre': u'Frazada Polar + Coj\xedn Relleno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3324204?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/3324204/Alisador-Midi-Travel?skuId=&passedNavAction=', 'nombre': u'Alisador Midi Travel', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2683098?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$9.990', 'link': u'http://www.falabella.com/falabella-cl/product/2683098/Alisador-Handy?skuId=&passedNavAction=', 'nombre': u'Alisador Handy', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3068490?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$11.990', 'link': u'http://www.falabella.com/falabella-cl/product/3068490/Maquina-de-Hilos-para-el-Cabello?skuId=&passedNavAction=', 'nombre': u'Maquina de Hilos para el Cabello', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370780?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370780/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-chocolate?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3370779?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3370779/Set-2-Toallas-ba\xf1o-600-gramos-+-toalla-de-visita-Beige?skuId=&passedNavAction=', 'nombre': u'Set 2 Toallas ba\xf1o 600 gramos + to...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2708416?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2708416/Alisador-Hp-8310?skuId=&passedNavAction=', 'nombre': u'Alisador Hp 8310', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3280914?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3280914/Alisador-CP1-STD-Blanco?skuId=&passedNavAction=', 'nombre': u'Alisador CP1 STD Blanco', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3003858?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3003858/Alisador-Pocket-Zebra-Sg-3350?skuId=&passedNavAction=', 'nombre': u'Alisador Pocket Zebra Sg-3350', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3004893?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/3004893/Prepara-y-sirva-el-desayuno-?skuId=&passedNavAction=', 'nombre': u'Prepara y sirva el desayuno', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/2388888?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$12.990', 'link': u'http://www.falabella.com/falabella-cl/product/2388888/Juego-Clue-Reinvencion-Quien-Es-el-Culpable?skuId=&passedNavAction=', 'nombre': u'Juego Clue Reinvenci\xf3n Qui\xe9n Es el...', 'desc': ''}, {'img': u'http://falabella.scene7.com/is/image/Falabella/3184374?$lista160$', 'likeAsociado': u'Lucho, el hermano desconocido de Jes\xfas', 'precio': u'$14.990', 'link': u'http://www.falabella.com/falabella-cl/product/3184374/Alisador--HP8333?skuId=&passedNavAction=', 'nombre': u'Alisador HP8333', 'desc': ''}]} 
	
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
	
	recs = dict(rbooks.items() + rmusic.items() + rmovies.items() + rgames.items())

	if len(recs) > 0:
		tieneLikes = True
	else:
		tieneLikes = False

	picture = request.session["picture"]
	user = request.session["user"]
	
	friendName = getFriendName(request.session['access_token'],id)
	
	return render_to_response("friendsLikes.html", {'recommendations' : recs, 'tieneLikes' : tieneLikes, 'picture':picture, 'user':user, 'friendName':friendName}) 

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
