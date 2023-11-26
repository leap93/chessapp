from django.shortcuts import render
from django.contrib.auth import logout

def logoutpage(request):
	logout(request)
	return render(request, 'chessapp/logout.html')
			
	