from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chessapp.models import Game, Move
from django.utils import timezone
@login_required
def new_game(request):
	if request.method == 'POST':
		game = Game(start_date = timezone.now())
		opponent = User.objects.get(username = request.POST.get('opponent'))
		if request.POST.get('color') == "w":
			game.white_player = request.user
			game.black_player = opponent
		else:
			game.black_player = request.user
			game.white_player = opponent
		game.save()
		
		return redirect("/chessapp/games?id=" + str(game.id))
	
	else:
		players = User.objects.all()
		current_player = request.user
		return render(request, 'chessapp/new_game.html', {"players": players, "current_player": current_player})	