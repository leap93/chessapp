from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as loginuser


def login(request):

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			loginuser(request, user)
			next = request.POST['next']
			if next != '':
				return render(request, next[1:]+'.html')
			else:
				return redirect("/chessapp/games")
		else:
			return render(request, 'chessapp/login.html', {'username' : username, 'message' : 'Invalid username or password', 'next' : request.POST['next']})
	
	if request.method == 'GET':
		if 'next' in request.GET:
			return render(request, 'chessapp/login.html', {'next' : request.GET['next'], 'message' : 'This pages requires a login'})
		else:
			return render(request, 'chessapp/login.html')
			
	