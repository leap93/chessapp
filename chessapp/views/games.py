from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chessapp.models import Game, Move
from django.views.decorators.csrf import csrf_exempt	
from django.utils import timezone
from chessapp.templatetags.extras import is_legal_move, move_causes_check
@login_required
@csrf_exempt
def games(request):
	#moves = Move.objects.all()
	#moves[len(moves)-1].delete()
	#for move in moves:
	#	move.delete()
	
	message = ''
	id = request.GET.get('id')
	
	if id is not None:
		game = Game.objects.filter(id = id)[0]
		
		player_color = "b"
		if game.white_player == request.user:
			player_color = "w"
		
		#Initializing board from the start. Board index goes from 0 to 7 and y comes before x
		board = [["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]]
		board.insert(2, ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"])
		for x in range(2,6):
			board.insert(x, [ "", "", "", "", "", "", "", ""])
		board.insert(6, ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"])
		board.insert(7, ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"])

		moves = Move.objects.filter(game=game)
		#execute all moves to the board
		for move in moves:
			board[int(move.to_square[1])][int(move.to_square[0])] = board[int(move.from_square[1])][int(move.from_square[0])]
			board[int(move.from_square[1])][int(move.from_square[0])] = ""
		
		
		#execute the move if method is post
		if request.method == 'POST':
			if is_legal_move(board, request.POST.get('fromX'), request.POST.get('fromY'), request.POST.get('toX'), request.POST.get('toY'), player_color) and not move_causes_check(board, {"fromX": int(request.POST.get('fromX')), "fromY": int(request.POST.get('fromY')), "toX": int(request.POST.get('toX')), "toY": int(request.POST.get('toY'))}):
				move = Move(game = game, move_date = timezone.now(), is_white = player_color == "w", from_square = request.POST.get('fromX') + request.POST.get('fromY'), to_square = request.POST.get('toX') + request.POST.get('toY'))
				move.save()	
				#execute the newest move
				board[int(move.to_square[1])][int(move.to_square[0])] = board[int(move.from_square[1])][int(move.from_square[0])]
				board[int(move.from_square[1])][int(move.from_square[0])] = ""
				#reset the moves set so it has the most recent move
				moves = Move.objects.filter(game=game)
			else:
				message = "Illegal move! "
		
		#assigning square colors
		for y in range(0,8):
			for x in range(0,8):
				board[y][x] =  squareColor(y, x) + board[y][x]
		
		players_turn = True
		if len(moves) > 0:
			lastMove = moves[len(moves)-1]
			
			#marking the last move with red squares
			board[int(lastMove.to_square[1])][int(lastMove.to_square[0])] = "r" + board[int(lastMove.to_square[1])][int(lastMove.to_square[0])][1:] 
			board[int(lastMove.from_square[1])][int(lastMove.from_square[0])] = "r" + board[int(lastMove.from_square[1])][int(lastMove.from_square[0])][1:]
			
			#if the previous turn was the same color as the player
			if lastMove.is_white != (player_color == "w"):
				message = message + "it's your turn"
			else:
				message = "waiting for oppoent's move..."
				players_turn = False
		elif player_color == "w":
			message = message + "it's your turn"
		else:
			message = "waiting for oppoent's move..."
			players_turn = False
		return render(request, 'chessapp/game.html', {"game" : game, "board" : board, "message" : message, "players_turn": players_turn, "player_color": player_color})
	else:
		games1 = Game.objects.filter(white_player=request.user, end_date__isnull=True)
		games2 = Game.objects.filter(black_player=request.user, end_date__isnull=True)
		return render(request, 'chessapp/games.html', {"games1" : games1, "games2" : games2})	
		
def squareColor(x, y):
	if (y%2==1 and x%2 == 1) or (y%2==0 and x%2 == 0):
		return "b";
	else:
		return "w";
		

		