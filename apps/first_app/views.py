from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import *
import bcrypt

# Create your views here.
def index(request):
	return render(request, "login.html")

def register(request):
	if request.method == "POST":
		errors = User.objects.basic_validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			return redirect('/')
		else:
			request.session['name'] = request.POST['first_name']
			user = User.objects.create()
			user.first_name = request.POST['first_name']
			user.last_name = request.POST['last_name']
			user.email = request.POST['email']
			user.password = bcrypt.hashpw(request.POST['password1'].encode(), bcrypt.gensalt())
			user.save()
			request.session['id'] = User.objects.get()
			return redirect('/success')

def login(request):
	if request.method == "POST":
		user = User.objects.get(email = request.POST['loginemail'])
		request.session['name'] = user.first_name
		request.session['id'] = user.id
		if bcrypt.checkpw(request.POST['loginpw'].encode(), user.password.encode()):
			return redirect('/success')
		else:
			errors = User.objects.login_validation(request.POST)
			if len(errors):
				for key, value in errors.items():
					messages.error(request, value)
				return redirect('/')

def success(request):
	if "id" not in request.session:
		return redirect('/')
	else:
		return render(request, "success.html")

def logout(request):
	return redirect('/')