from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chessapp.models import Game, Move
from django.utils import timezone
@login_required
def new_game(request):
	if request.method == 'POST':
		opponent = User.objects.get(username = request.POST.get('opponent'))
		existing_games1 = Game.objects.filter(white_player=request.user, black_player=opponent, end_date__isnull=True)
		existing_games2 = Game.objects.filter(black_player=request.user, white_player=opponent, end_date__isnull=True)
		if len(existing_games1) > 0 or len(existing_games2) > 0:
			players = User.objects.all()
			current_player = request.user
			return render(request, 'chessapp/new_game.html', {"players": players, "current_player": current_player, "message": "please finnish a game with that player before starting a new one"})					
		game = Game(start_date = timezone.now())		
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