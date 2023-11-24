from django.http import HttpResponse
from django.shortcuts import render
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from chessapp.models import Confirmation
def registeration(request):

	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		try:
			user = User.objects.create_user(username, email , password)
		except IntegrityError: 
			return render(request, 'chessapp/register.html', {'message' : 'User ' + username + ' already exists.', 'first_name' : first_name, 'last_name' : last_name, 'email' : email})
		user.first_name = first_name
		user.last_name = last_name
		user.save()
		code = 123456
		
		confirmation = Confirmation.objects.create(user = user, confirmation_code = code)
		
		send_mail(
			"Your confirmation code",
			"Your confimration code is " + str(code),
			"chessapp@chessapp.com",
			[email],
			fail_silently=False,
		)
		
		
		
		return render(request, 'chessapp/email_confirmation.html', {'message' : 'Registeration successful!'})


	if request.method == 'GET':
		return render(request, 'chessapp/register.html')