from django.test import TestCase
from chessapp.templatetags.extras import *
from chessapp.models import Game, Move
from django.utils import timezone
from django.contrib.auth.models import User

def start_board():
	board = [["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]]
	board.insert(2, ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"])
	for x in range(2,6):
		board.insert(x, [ "", "", "", "", "", "", "", ""])
	board.insert(6, ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"])
	board.insert(7, ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"])
	return board

def empty_board():
	board = []
	for x in range(0,8):
		board.insert(x, [ "", "", "", "", "", "", "", ""])
	return board

class TestPawnLegalMoves(TestCase):
	#pawn moving staight
	def test_move_pawn_1(self):
		self.assertTrue(is_legal_move(start_board(), 1, 1, 1, 2, "w", ""))
	#pawn double move from the start square
	def test_move_pawn_2(self):
		self.assertTrue(is_legal_move(start_board(), 1, 1, 1, 3, "w", ""))		
	#pawn moving diagonally without a capture
	def test_move_pawn_3(self):
		self.assertFalse(is_legal_move(start_board(), 1, 1, 2, 2, "w", ""))			
	#pawn moving diagonally with a capture
	def test_move_pawn_4(self):
		board = start_board()
		board[2][2] = "bpawn"
		self.assertTrue(is_legal_move(board, 1, 1, 2, 2, "w", ""))		
	#pawn moving staight trying to capture
	def test_move_pawn_5(self):
		board = start_board()
		board[2][2] = "bpawn"
		self.assertFalse(is_legal_move(board, 2, 1, 2, 2, "w", ""))	

		
class TestKnightLegalMoves(TestCase):
	#knight moving corretly
	def test_move_knight_1(self):
		self.assertTrue(is_legal_move(start_board(), 1, 0, 2, 2, "w", ""))
	#knight trying to capture own piece
	def test_move_knight_2(self):
		self.assertFalse(is_legal_move(start_board(), 1, 0, 3, 1, "w", ""))		
	#knight captures an opponent piece
	def test_move_knight_3(self):
		board = start_board()
		board[2][2] = "bpawn"
		self.assertTrue(is_legal_move(start_board(), 1, 0, 2, 2, "w", ""))		
	
class TestBishopLegalMoves(TestCase):
	#bishop tries to move when there is a piece along the path
	def test_move_bishop_1(self):
		self.assertFalse(is_legal_move(start_board(), 2, 0, 0, 2, "w", ""))
	#bishop moving correctly
	def test_move_bishop_2(self):
		board = start_board()
		board[1][1] = ""
		self.assertTrue(is_legal_move(board, 2, 0, 0, 2, "w", ""))		
	#bishop captures
	def test_move_bishop_3(self):
		board = start_board()
		board[1][1] = ""
		board[2][0] = "bpawn"
		self.assertTrue(is_legal_move(board, 2, 0, 0, 2, "w", ""))			
	#bishop trying to move incorrectly
	def test_move_bishop_4(self):
		board = start_board()
		board[1][2] = ""
		board[1][3] = ""
		self.assertFalse(is_legal_move(board, 2, 0, 4, 3, "w", ""))	
		
class TestRookLegalMoves(TestCase):
	#rook tries to move when there is a piece along the path
	def test_move_rook_1(self):
		self.assertFalse(is_legal_move(start_board(), 0, 0, 0, 2, "w", ""))
	#rook moving correctly
	def test_move_rook_2(self):
		board = start_board()
		board[1][0] = ""
		self.assertTrue(is_legal_move(board, 0, 0, 0, 4, "w", ""))		
	#rook captures
	def test_move_rook_3(self):
		board = start_board()
		board[1][0] = ""
		self.assertTrue(is_legal_move(board, 0, 0, 0, 6, "w", ""))			
	#rook trying to move incorrectly
	def test_move_rook_4(self):
		board = start_board()
		board[1][0] = ""
		board[1][1] = ""
		self.assertFalse(is_legal_move(board, 0, 0, 2, 2, "w", ""))	
		
class TestKingLegalMoves(TestCase):
	def setUp(self):
		white_player = User.objects.create_user("One", "test@test.com", "testpassword")
		white_player.save()
		black_player = User.objects.create_user("Two", "test@test.com", "testpassword")
		black_player.save()		
		Game.objects.create(white_player = white_player, black_player = black_player, start_date = timezone.now())
	
	#king tries to capture it's own piece
	def test_move_king_1(self):
		self.assertFalse(is_legal_move(start_board(), 4, 0, 0, 3, "w", Game.objects.all()[0]))
	#king moving correctly
	def test_move_king_2(self):
		board = start_board()
		board[1][4] = ""
		self.assertTrue(is_legal_move(board, 4, 0, 4, 1, "w", Game.objects.all()[0]))		
	#king captures
	def test_move_king_3(self):
		board = start_board()
		board[1][4] = "bpawn"
		self.assertTrue(is_legal_move(board, 4, 0, 4, 1, "w", Game.objects.all()[0]))			
	#king trying to move incorrectly
	def test_move_king_4(self):
		board = start_board()
		board[1][4] = ""
		board[1][5] = ""
		self.assertFalse(is_legal_move(board, 4, 0, 2, 5, "w", Game.objects.all()[0]))	

	#king short castle fail
	def test_move_king_5(self):
		board = start_board()
		board[0][5] = ""
		self.assertFalse(is_legal_move(board, 4, 0, 6, 0, "w", Game.objects.all()[0]))	
		
	#king short castle success
	def test_move_king_5(self):
		board = start_board()
		board[0][5] = ""
		board[0][6] = ""
		self.assertTrue(is_legal_move(board, 4, 0, 6, 0, "w", Game.objects.all()[0]))

	#king long castle fail
	def test_move_king_6(self):
		board = start_board()
		board[0][5] = ""
		self.assertFalse(is_legal_move(board, 4, 0, 1, 0, "w", Game.objects.all()[0]))	
		
	#king long castle success
	def test_move_king_7(self):
		board = start_board()
		board[0][1] = ""
		board[0][2] = ""
		board[0][3] = ""	
		self.assertTrue(is_legal_move(board, 4, 0, 2, 0, "w", Game.objects.all()[0]))			
		
class TestAllMovesGeneration(TestCase):
		
	#all moves with the initial board
	def test_all_moves_1(self):
		board = start_board()
		self.assertEquals(len(all_legal_moves(board, "w")), 20)

	#all moves with inital board and pawn taken out at E2
	def test_all_moves_2(self):
		board = start_board()
		board[1][4] = ""
		self.assertEquals(len(all_legal_moves(board, "w")), 29)	
	
	#all moves with inital board and pawn taken out at A2 and D2
	def test_all_moves_3(self):
		board = start_board()
		board[1][0] = ""
		board[1][3] = ""
		self.assertEquals(len(all_legal_moves(board, "w")), 35)		

class TestKingFinder(TestCase):
	
	#king in the starting position
	def test_king_finder_1(self):
		board = start_board()
		self.assertEquals(find_king(board, "w"), {"x" : 4, "y": 0})

	#king in the middle of the board
	def test_king_finder_2(self):
		board = start_board()
		board[4][4] = "wking"
		board[0][4] = ""
		self.assertEquals(find_king(board, "w"), {"x" : 4, "y": 4})	

class TestCheckChecker(TestCase):
	
	#move that does not cause check
	def test_check_checker_1(self):
		board = empty_board()
		board[4][4] = "wking"
		board[7][7] = "bking"
		board[7][6] = "bqueen"
		self.assertFalse(move_causes_check(board, {"fromX": 4, "fromY": 4, "toX": 5, "toY": 5}))

	#move that causes check 1 
	def test_check_checker_2(self):
		board = empty_board()
		board[4][4] = "wking"
		board[7][7] = "bking"
		board[7][5] = "bqueen"
		self.assertTrue(move_causes_check(board, {"fromX": 4, "fromY": 4, "toX": 5, "toY": 5}))

	#move that causes check 2 
	def test_check_checker_3(self):
		board = empty_board()
		board[4][4] = "wking"
		board[4][5] = "wknight"
		board[7][7] = "bking"
		board[4][6] = "bqueen"
		self.assertTrue(move_causes_check(board, {"fromX": 5, "fromY": 4, "toX": 3, "toY": 3}))
	
class TestMoveMaker(TestCase):

	#move 1 
	def test_move_maker_1(self):
		board = start_board()
		make_move(board, {"fromX": 1, "fromY": 0, "toX": 2, "toY": 2})
		self.assertEquals(board[2][2], "wknight")
		self.assertEquals(board[0][1], "")
		
	#move 2 
	def test_move_maker_2(self):
		board = start_board()
		board[4][4] = "wrook"
		make_move(board, {"fromX": 4, "fromY": 4, "toX": 4, "toY": 6})
		self.assertEquals(board[6][4], "wrook")
		self.assertEquals(board[4][4], "")
		
	#short castling white
	def test_move_maker_3(self):
		board = start_board()
		board[0][5] = ""
		board[0][6] = ""
		make_move(board, {"fromX": 4, "fromY": 0, "toX": 6, "toY": 0})
		self.assertEquals(board[0][4], "")
		self.assertEquals(board[0][5], "wrook")
		self.assertEquals(board[0][6], "wking")
		self.assertEquals(board[0][7], "")	
		
	#long castling white
	def test_move_maker_4(self):
		board = start_board()
		board[0][1] = ""
		board[0][2] = ""
		board[0][3] = ""
		make_move(board, {"fromX": 4, "fromY": 0, "toX": 2, "toY": 0})
		self.assertEquals(board[0][0], "")
		self.assertEquals(board[0][1], "")
		self.assertEquals(board[0][2], "wking")
		self.assertEquals(board[0][3], "wrook")			
		self.assertEquals(board[0][4], "")
		
	#short castling black
	def test_move_maker_5(self):
		board = start_board()
		board[7][5] = ""
		board[7][6] = ""
		make_move(board, {"fromX": 4, "fromY": 7, "toX": 6, "toY": 7})
		self.assertEquals(board[7][4], "")
		self.assertEquals(board[7][5], "brook")
		self.assertEquals(board[7][6], "bking")
		self.assertEquals(board[7][7], "")	
		
	#long castling black
	def test_move_maker_6(self):
		board = start_board()
		board[7][1] = ""
		board[7][2] = ""
		board[7][3] = ""
		make_move(board, {"fromX": 4, "fromY": 7, "toX": 2, "toY": 7})
		self.assertEquals(board[7][0], "")
		self.assertEquals(board[7][1], "")
		self.assertEquals(board[7][2], "bking")
		self.assertEquals(board[7][3], "brook")			
		self.assertEquals(board[7][4], "")		

	#white pawn into queen 
	def test_move_maker_7(self):
		board = start_board()
		board[6][0] = "wpawn"
		board[6][1] = ""
		board[7][0] = ""
		board[7][1] = ""
		
		make_move(board, {"fromX": 0, "fromY": 6, "toX": 0, "toY": 7})
		self.assertEquals(board[7][0], "wqueen")
		self.assertEquals(board[6][0], "")

	#black pawn into queen 
	def test_move_maker_8(self):
		board = start_board()
		board[1][0] = "bpawn"
		board[1][1] = ""
		board[0][0] = ""
		board[0][1] = ""
		
		make_move(board, {"fromX": 0, "fromY": 1, "toX": 0, "toY": 0})
		self.assertEquals(board[0][0], "bqueen")
		self.assertEquals(board[1][0], "")
		
class TestMoveUnmaker(TestCase):

	#move 1 
	def test_move_unmaker_1(self):
		board = start_board()
		destination = make_move(board, {"fromX": 1, "fromY": 0, "toX": 2, "toY": 2})
		undo_move(board, {"fromX": 1, "fromY": 0, "toX": 2, "toY": 2}, destination)
		self.assertEquals(board[2][2], "")
		self.assertEquals(board[0][1], "wknight")
		
	#move 2 
	def test_move_unmaker_2(self):
		board = start_board()
		board[4][4] = "wrook"
		destination = make_move(board, {"fromX": 4, "fromY": 4, "toX": 4, "toY": 6})
		undo_move(board, {"fromX": 4, "fromY": 4, "toX": 4, "toY": 6}, destination)
		self.assertEquals(board[6][4], "bpawn")
		self.assertEquals(board[4][4], "wrook")
		
	#short castling white
	def test_move_unmaker_3(self):
		board = start_board()
		board[0][5] = ""
		board[0][6] = ""
		destination = make_move(board, {"fromX": 4, "fromY": 0, "toX": 6, "toY": 0})
		undo_move(board, {"fromX": 4, "fromY": 0, "toX": 6, "toY": 0}, destination)
		self.assertEquals(board[0][4], "wking")
		self.assertEquals(board[0][5], "")
		self.assertEquals(board[0][6], "")
		self.assertEquals(board[0][7], "wrook")	
		
	#long castling white
	def test_move_unmaker_4(self):
		board = start_board()
		board[0][1] = ""
		board[0][2] = ""
		board[0][3] = ""
		destination = make_move(board, {"fromX": 4, "fromY": 0, "toX": 2, "toY": 0})
		undo_move(board, {"fromX": 4, "fromY": 0, "toX": 2, "toY": 0}, destination)
		self.assertEquals(board[0][0], "wrook")
		self.assertEquals(board[0][1], "")
		self.assertEquals(board[0][2], "")
		self.assertEquals(board[0][3], "")			
		self.assertEquals(board[0][4], "wking")
		
	#short castling black
	def test_move_unmaker_5(self):
		board = start_board()
		board[7][5] = ""
		board[7][6] = ""
		destination = make_move(board, {"fromX": 4, "fromY": 7, "toX": 6, "toY": 7})
		undo_move(board, {"fromX": 4, "fromY": 7, "toX": 6, "toY": 7}, destination)
		self.assertEquals(board[7][4], "bking")
		self.assertEquals(board[7][5], "")
		self.assertEquals(board[7][6], "")
		self.assertEquals(board[7][7], "brook")	
		
	#long castling black
	def test_move_unmaker_6(self):
		board = start_board()
		board[7][1] = ""
		board[7][2] = ""
		board[7][3] = ""
		destination = make_move(board, {"fromX": 4, "fromY": 7, "toX": 2, "toY": 7})
		undo_move(board, {"fromX": 4, "fromY": 7, "toX": 2, "toY": 7}, destination)
		self.assertEquals(board[7][0], "brook")
		self.assertEquals(board[7][1], "")
		self.assertEquals(board[7][2], "")
		self.assertEquals(board[7][3], "")			
		self.assertEquals(board[7][4], "bking")	

	#white pawn into queen 
	def test_move_unmaker_7(self):
		board = start_board()
		board[6][0] = "wpawn"
		board[6][1] = ""
		board[7][0] = ""
		board[7][1] = ""
		
		destination = make_move(board, {"fromX": 0, "fromY": 6, "toX": 0, "toY": 7})
		undo_move(board, {"fromX": 0, "fromY": 6, "toX": 0, "toY": 7}, destination)
		self.assertEquals(board[7][0], "")
		self.assertEquals(board[6][0], "wpawn")

	#black pawn into queen 
	def test_move_unmaker_8(self):
		board = start_board()
		board[1][0] = "bpawn"
		board[1][1] = ""
		board[0][0] = ""
		board[0][1] = ""
		
		destination = make_move(board, {"fromX": 0, "fromY": 1, "toX": 0, "toY": 0})
		undo_move(board, {"fromX": 0, "fromY": 1, "toX": 0, "toY": 0}, destination)
		self.assertEquals(board[0][0], "")
		self.assertEquals(board[1][0], "bpawn")

		