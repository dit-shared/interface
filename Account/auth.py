from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User, HashPassword
import json

def buildJSONRespose(responseData):
	return HttpResponse(json.dumps(responseData), content_type="application/json")

def auth(request):
	if 'id' in request.session:
		return HttpResponseRedirect('/account')
	return render(request, 'Authorize/auth.html')

def login(request):
	response = {"success": False, }
	if 'login' not in request.POST or 'passwd' not in request.POST:
		response["message"] = "Неправильный POST запрос"
		return buildJSONRespose(response)
	login, passwd = request.POST['login'], request.POST['passwd']
	if User.objects.filter(login=login):
		user = User.objects.filter(login=login)[0]
		if user.passwd == HashPassword(passwd):
			response['redirect'] = '/account'
			response['success'] = True
			request.session['id'] = user.id
	response['message'] = 'Неправильный логин или пароль!'
	return buildJSONRespose(response)

def deAuth(request):
	if 'id' in request.session:
		del request.session['id']
	return HttpResponseRedirect('/')

def error_404(request, exception):
	return render(request, 'ServerError/index.html', {'error_type': 404, 'error_header': 'Page not found!'})

def error_500(request):
	return render(request, 'ServerError/index.html', {'error_type': 500, 'error_header': 'Internal server error'})

def check_error_page(request):
	return render(request, 'ServerError/index.html', {'error_type': 500, 'error_header': 'Internal server error'})