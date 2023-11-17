from django import template
import numpy as np
from chessapp.models import Game, Move
register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg	
	
def is_legal_move(board, fromX, fromY, toX, toY, player_color, game):
	fromX = int(fromX)
	fromY = int(fromY)
	toX = int(toX)
	toY = int(toY)
	
	#check that the selected square is not empty and has a correct player's piece
	if board[fromY][fromX] == "" or board[fromY][fromX][0] != player_color:
		return False
		
	piece = board[fromY][fromX]
	destination = board[toY][toX]
	
	type = piece[1:]
	if type == "pawn":
		return isLegalMovePawn(board, piece, destination, fromX, fromY, toX, toY)
	elif type == "knight":
		return isLegalMoveKnight(board, piece, destination, fromX, fromY, toX, toY)
	elif type == "bishop":
		return isLegalMoveBishop(board, piece, destination, fromX, fromY, toX, toY)
	elif type == "rook":
		return isLegalMoveRook(board, piece, destination, fromX, fromY, toX, toY)
	elif type == "queen":
		return isLegalMoveBishop(board, piece, destination, fromX, fromY, toX, toY) or isLegalMoveRook(board, piece, destination, fromX, fromY, toX, toY)		
	else:
		return isLegalMoveKing(board, piece, destination, fromX, fromY, toX, toY, game)
	
def isLegalMovePawn(board, piece, destination, fromX, fromY, toX, toY):	
	if piece[0] == "w":
		#2 square move from the starting position
		if fromY == 1 and fromY + 2 == toY and fromX == toX and destination == "" and board[toY - 1][toX] == "":
			return True
		#move forward to an empty square
		if fromY + 1 == toY and fromX == toX and destination == "":
			return True
		#pawn captures a piece
		if fromY + 1 == toY and abs(fromX - toX) == 1 and destination != "" and destination[0] == "b":
			return True					
	else:
		#2 square move from the starting position
		if fromY == 6 and fromY - 2 == toY and fromX == toX and destination == "" and board[toY + 1][toX] == "":
			return True
		#move forward to an empty square
		if fromY - 1 == toY and fromX == toX and destination == "":
			return True
		#pawn captures a piece
		if fromY - 1 == toY and abs(fromX - toX) == 1 and destination != "" and destination[0] == "w":
			return True	
	return False
	
def isLegalMoveKnight(board, piece, destination, fromX, fromY, toX, toY):
	#check if destination has own piece
	if destination != "" and destination[0] == piece[0]:
		return False
	if (abs(fromX - toX) == 2 and abs(fromY - toY) == 1) or (abs(fromX - toX) == 1 and abs(fromY - toY) == 2):
		return True
	return False		
	
def isLegalMoveBishop(board, piece, destination, fromX, fromY, toX, toY):
	#check if destination has own piece
	if destination != "" and destination[0] == piece[0]:
		return False
	#check that the move is diagonal
	if abs(fromX - toX) != abs(fromY - toY):
		return False
	
	#check that all squares along the path are empty
	for d in range(1, abs(fromX - toX)):
		if board[fromY+np.sign(toY - fromY)*d][fromX+np.sign(toX - fromX)*d] != "":
			return False			
	return True

def isLegalMoveRook(board, piece, destination, fromX, fromY, toX, toY):
	#check if destination has own piece
	if destination != "" and destination[0] == piece[0]:
		return False		
	#horizontal movement
	if fromY == toY:
		#check that all squares along the path are empty
		for d in range(1, abs(fromX - toX)):
			if board[fromY][fromX+np.sign(toX - fromX)*d] != "":
				return False
	#vertical movement
	elif fromX == toX:
		#check that all squares along the path are empty
		for d in range(1, abs(fromY - toY)):
			if board[fromY+np.sign(toY - fromY)*d][fromX] != "":
				return False								
	else:
		return False
	return True

def isLegalMoveKing(board, piece, destination, fromX, fromY, toX, toY, game):
	
	castlings = possible_castlings(game)
	#white long castle
	if castlings["white_long_castle"] and board[0][1] == "" and board[0][2] == "" and board[0][3] == "" and toX == 2 and toY == 0 and piece == "wking":
		return True
	#white short castle
	if castlings["white_short_castle"] and board[0][5] == "" and board[0][6] == "" and toX == 6 and toY == 0 and piece == "wking":
		return True

	
	#check if destination has own piece
	if destination != "" and destination[0] == piece[0]:
		return False
	#check if move is longer than 1 square
	if abs(fromX - toX) > 1 or abs(fromY - toY) > 1:
		return False
	return True
	

def all_legal_moves(board, color):
	moves = []
	for y in range(0,8):
		for x in range(0,8):
			if board[y][x] != "" and board[y][x][0] == color:
				if board[y][x][1:] == "knight":
					if y + 1 < 8 and x + 2 < 8 and isLegalMoveKnight(board, board[y][x], board[y + 1][x + 2], x, y, x + 2, y + 1):
						moves.append({"fromX": x, "fromY": y, "toX": x + 2, "toY": y + 1})
					if y + 1 < 8 and x - 2 > -1 and isLegalMoveKnight(board, board[y][x], board[y + 1][x - 2], x, y, x - 2, y + 1):
						moves.append({"fromX": x, "fromY": y, "toX": x - 2, "toY": y + 1})
					if y - 1 > -1 and x + 2 < 8 and isLegalMoveKnight(board, board[y][x], board[y - 1][x + 2], x, y, x + 2, y - 1):
						moves.append({"fromX": x, "fromY": y, "toX": x + 2, "toY": y - 1})
					if y - 1 > -1 and x - 2 > -1 and isLegalMoveKnight(board, board[y][x], board[y - 1][x - 2], x, y, x - 2, y - 1):
						moves.append({"fromX": x, "fromY": y, "toX": x - 2, "toY": y - 1})
					if y + 2 < 8 and x + 1 < 8 and isLegalMoveKnight(board, board[y][x], board[y + 2][x + 1], x, y, x + 1, y + 2):
						moves.append({"fromX": x, "fromY": y, "toX": x + 1, "toY": y + 2})
					if y + 2 < 7 and x - 1 > -1 and isLegalMoveKnight(board, board[y][x], board[y + 2][x - 1], x, y, x - 1, y + 2):
						moves.append({"fromX": x, "fromY": y, "toX": x - 1, "toY": y + 2})
					if y - 2 > -1 and x + 1 < 8 and isLegalMoveKnight(board, board[y][x], board[y - 2][x + 1], x, y, x + 1, y - 2):
						moves.append({"fromX": x, "fromY": y, "toX": x + 1, "toY": y - 2})
					if y - 2 > -1 and x - 1 > -1 and isLegalMoveKnight(board, board[y][x], board[y - 2][x - 1], x, y, x - 1, y - 2):
						moves.append({"fromX": x, "fromY": y, "toX": x - 1, "toY": y - 2})
				else:
					dy = y + 1
					while dy <= 7:
						if is_legal_move(board, x, y, x, dy, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x, "toY": dy})
						else:
							break
						dy = dy + 1
					dy = y - 1
					while dy >= 0:
						if is_legal_move(board, x, y, x, dy, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x, "toY": dy})
						else:
							break
						dy = dy - 1
					dx = x + 1
					while dx <= 7:
						if is_legal_move(board, x, y, dx, y, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": dx, "toY": y})
						else:
							break
						dx = dx + 1	
					dx = x - 1
					while dx >= 0:
						if is_legal_move(board, x, y, dx, y, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": dx, "toY": y})
						else:
							break
						dx = dx - 1
					d = 1 
					while x + d <= 7 and y + d <= 7:
						if is_legal_move(board, x, y, x + d, y + d, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x + d, "toY": y + d})
						else:
							break
						d = d + 1
					d = 1 
					while x - d >= 0 and y + d <= 7:
						if is_legal_move(board, x, y, x - d, y + d, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x - d, "toY": y + d})
						else:
							break
						d = d + 1
					d = 1	
					while x + d <= 7 and y - d >= 0:
						if is_legal_move(board, x, y, x + d, y - d, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x + d, "toY": y - d})
						else:
							break
						d = d + 1
					d = 1	
					while x - d >= 0 and y - d >= 0:
						if is_legal_move(board, x, y, x - d, y - d, color, None):
							moves.append({"fromX": x, "fromY": y, "toX": x - d, "toY": y - d})
						else:
							break
						d = d + 1					
	return moves			
		
def find_king(board, color):
	for y in range(0,8):
		for x in range(0,8):
			if board[y][x] == color + "king":
				return {"x" : x, "y": y}
	return {"x" : -1, "y": -1}
	
def move_causes_check(board, move):
	check = False
	#color of the opponent
	color = "b"
	opponent = "w"
	
	move["fromX"] = int(move["fromX"])
	move["fromY"] = int(move["fromY"])
	move["toX"] = int(move["toX"])
	move["toY"] = int(move["toY"])
	
	if board[move["fromY"]][move["fromX"]][0] == "w":
		color = "w"
		opponent = "b"
	
	#make the move
	destination = make_move(board, move)

	
	#check all the opponent's moves if any of them captures the king
	king = find_king(board, color)
	all_moves = all_legal_moves(board, opponent)
	for checking_move in all_moves:
		if checking_move["toY"] == king["y"] and checking_move["toX"] == king["x"]:
			check = True
			break
			
	#undo the move
	undo_move(board, move, destination)

	return check
				
def pick_move(board, color, dept):

	max_move = ""
	max_score = 0
	opponent = "b";
	if color == "w":
		moves = all_legal_moves(board, color)
		max_score = -1000000000
	else:
		opponent = "w"
		moves = all_legal_moves(board, color)
		max_score = 1000000000

	for move in moves:
		if dept == 3 and move_causes_check(board, move):
			continue
		
		#make the move
		destination = make_move(board, move)	
		
		if dept == 1:
			score = scoreBoard(board)
		else:
			score = pick_move(board, opponent, dept-1)[1]
			
		if (color == "w" and score > max_score) or (color == "b" and score < max_score):
			max_move = move
			max_score = score
		#undo the move
		undo_move(board, move, destination)	
	return (max_move, max_score)

	
def make_move(board, move):
	destination = board[move["toY"]][move["toX"]]
	board[move["toY"]][move["toX"]] = board[move["fromY"]][move["fromX"]]
	board[move["fromY"]][move["fromX"]] = ""
	#white long castle
	if move["fromX"] == 4 and move["fromY"] == 0 and move["toX"] == 2 and move["toY"] == 0:
		board[0][3] = board[0][0]
		board[0][0] = ""
	#white short castle
	if move["fromX"] == 4 and move["fromY"] == 0 and move["toX"] == 6 and move["toY"] == 0:
		board[0][5] = board[0][7]
		board[0][7] = ""

	return destination
	
def undo_move(board, move, destination):
	board[move["fromY"]][move["fromX"]] = board[move["toY"]][move["toX"]]
	board[move["toY"]][move["toX"]] = destination	
	#white long castle
	if move["fromX"] == 4 and move["fromY"] == 0 and move["toX"] == 2 and move["toY"] == 0:
		board[0][0] = board[0][3]
		board[0][3] = ""	
	#white short castle
	if move["fromX"] == 4 and move["fromY"] == 0 and move["toX"] == 6 and move["toY"] == 0:
		board[0][7] = board[0][5]
		board[0][5] = ""

def scoreBoard(board):
	score = 0
	pieces = []
	for y in range(0,8):
		for x in range(0,8):
			if(board[y][x] != ""):
				pieces.append({"x" : x, "y" : y})
	for piece in pieces:
		piece_text = board[piece["y"]][piece["x"]]
		type = piece_text[1:]
		color = piece_text[0]

		#pawn score based on it's placement on board
		if type == "pawn":
			if color == "w":						
				if piece["y"] == 7:
					score = score + 80
				else:
					score = score + piece["y"] + 10	
			else:
				if piece["y"] == 0:
					score = score - 80
				else:
					score = score + piece["y"] - 7 - 10
		
		pointing = 0
		#material score
		if type == "knight" or type == "bishop":
			pointing = 30
		elif type == "rook":
			pointing = 50			
		elif type == "queen":
			pointing = 80				
		elif type == "king":
			pointing = 10000
			adj_score = 3
			#King security evaluation
			for dx in range(-1, 2):
				for dy in range(-1, 2):
					if piece["x"] + dx > 7 or piece["x"] + dx < -1 or piece["y"] + dy > 7 or piece["y"] + dy < -1:
						continue
					
					adjScorePiece = board[piece["y"] + dy][piece["x"] + dx]
					if color == "w":
						if adjScorePiece != "" and adjScorePiece[0] == "w":
							score = score + adj_score
					else:
						if adjScorePiece != "" and adjScorePiece[0] == "b":
							score = score - adj_score

		if color == "w":
			score = score + pointing
		else:
			score = score - pointing	
	return score
	
def possible_castlings(game):
	white_short_castle = True
	white_long_castle = True
	black_short_castle = True
	black_long_castle = True
	
	moves = Move.objects.filter(game=game)
	
	for move in moves:
		if move.from_square == "00" or move.to_square == "00":
			white_long_castle = False
		if move.from_square == "40":
			white_short_castle = False
			white_long_castle = False			
		if move.from_square == "70" or move.to_square == "70":
			white_short_castle = False
		if move.from_square == "07" or move.to_square == "07":
			black_long_castle = False
		if move.from_square == "47":
			black_short_castle = False
			black_long_castle = False			
		if move.from_square == "77" or move.to_square == "77":
			black_short_castle = False			
	return {"white_short_castle" : white_short_castle, "white_long_castle" : white_long_castle, "black_short_castle" : black_short_castle, "black_long_castle" : black_long_castle}
	