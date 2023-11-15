from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chessapp.models import Game, Move
from django.views.decorators.csrf import csrf_exempt	
from django.utils import timezone
from chessapp.templatetags.extras import is_legal_move, move_causes_check, pick_move, possible_castlings, all_legal_moves
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
		opponent_color = "w"
		if game.white_player == request.user:
			player_color = "w"
			opponent_color = "b"
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
			execute_move(board, move)
			
		fromX = request.POST.get('fromX')
		fromY = request.POST.get('fromY')
		toX = request.POST.get('toX')
		toY = request.POST.get('toY')
		
		#execute the move if method is post
		if request.method == 'POST':
			if is_legal_move(board, fromX, fromY, toX, toY, player_color, game) and not move_causes_check(board, {"fromX": fromX, "fromY": fromY, "toX": toX, "toY": toY}):
				move = Move(game = game, move_date = timezone.now(), is_white = player_color == "w", from_square = request.POST.get('fromX') + request.POST.get('fromY'), to_square = request.POST.get('toX') + request.POST.get('toY'))
				move.save()	
				#execute the newest move
				execute_move(board, move)

				#execute CPU move
				if game.black_player.username == "CPU" or game.white_player.username == "CPU":
					opponent_move = pick_move(board, opponent_color, 3)[0]
					
					#CPU has no legal moves -> victory
					if opponent_move == "":
						game.end_date = timezone.now()
						if player_color == "w":
							game.winner = game.white_player 
						else:
							game.winner = game.black_player
						game.save()					
					else:
						move = Move(game = game, move_date = timezone.now(), is_white = player_color != "w", from_square = str(opponent_move["fromX"]) + str(opponent_move["fromY"]), to_square = str(opponent_move["toX"]) + str(opponent_move["toY"]))
						move.save()	
						#execute the newest move to the board
						execute_move(board, move)
				#reset the moves set so it has the new move(s)
				moves = Move.objects.filter(game=game)				
			
			else:
				message = "Illegal move! "
		
		#gather all possible moves for the player
		all_possible_moves = all_legal_moves(board, player_color)
		filetered_moves = []
		for move in all_possible_moves:
			if not move_causes_check(board, move):
				filetered_moves.append(move)
		
		#game ends to a defeat
		if len(filetered_moves) == 0 and game.end_date == None:
			game.end_date = timezone.now()
			if opponent_color == "w":
				game.winner = game.white_player 
			else:
				game.winner = game.black_player
			game.save()
		
		#assigning square colors
		for y in range(0,8):
			for x in range(0,8):
				board[y][x] =  squareColor(y, x) + board[y][x]
		
		players_turn = True
		lastMove = ""
		if len(moves) > 0:
			lastMove = moves[len(moves)-1]

			#game has ended
			if not game.end_date == None:
				players_turn = False
				if game.winner == request.user:
					message = "This game is over. You won!"	
				else:
					message = "This game is over. You lost!"	
			#player's turn
			elif lastMove.is_white != (player_color == "w"):
				message = message + "it's your turn"
			#opponent's turn
			else:
				message = "waiting for oppoent's move..."
				players_turn = False
		elif player_color == "w":
			message = message + "it's your turn"
		else:
			message = "waiting for oppoent's move..."
			players_turn = False
		return render(request, 'chessapp/game.html', {"game" : game, "board" : board, "message" : message, "players_turn": players_turn, "player_color": player_color, "moves": filetered_moves, "last_move" : lastMove})
	else:
		games1 = Game.objects.filter(white_player=request.user, end_date__isnull=True)
		games2 = Game.objects.filter(black_player=request.user, end_date__isnull=True)
		games3 = Game.objects.filter(white_player=request.user, end_date__isnull=False)
		games4 = Game.objects.filter(black_player=request.user, end_date__isnull=False)		
		return render(request, 'chessapp/games.html', {"games1" : games1, "games2" : games2, "games3" : games3, "games4" : games4})	
		
def squareColor(x, y):
	if (y%2==1 and x%2 == 1) or (y%2==0 and x%2 == 0):
		return "b";
	else:
		return "w";
		

def execute_move(board, move):
	board[int(move.to_square[1])][int(move.to_square[0])] = board[int(move.from_square[1])][int(move.from_square[0])]
	board[int(move.from_square[1])][int(move.from_square[0])] = ""
	#white long castle
	if move.from_square[0] == "4" and move.from_square[1] == "0" and move.to_square[0] == "2" and move.to_square[1] == "0":
		board[0][3] = board[0][0]
		board[0][0] = ""
	#white short castle
	if move.from_square[0] == "4" and move.from_square[1] == "0" and move.to_square[0] == "6" and move.to_square[1] == "0":
		board[0][5] = board[0][7]
		board[0][7] = ""
			