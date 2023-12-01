from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chessapp.models import Game, Message
from django.utils import timezone

@login_required
def messages(request):
	id = request.POST.get('id')
	if id is not None:
		game = Game.objects.filter(id = id)
		if len(game) == 0:
			return render(request, 'chessapp/error.html', {"message" : "Game ID is invalid"})
		game = game[0]	
		if not game.white_player == request.user and not game.black_player == request.user:
			return render(request, 'chessapp/error.html', {"message" : "You are not participating in this game."})

		message = Message(game = game, send_date = timezone.now(), sender = request.user, message = request.POST.get('message'))
		message.save()
		return redirect("/chessapp/games?id=" + str(game.id))

	else:
		return render(request, 'chessapp/error.html', {"message" : "The game does not exist!"})