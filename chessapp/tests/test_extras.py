from django.test import TestCase
from chessapp.templatetags.extras import is_legal_move, move_causes_check, pick_move, possible_castlings, all_legal_moves


def start_board():
	board = [["wrook", "wknight", "wbishop", "wqueen", "wking", "wbishop", "wknight", "wrook"]]
	board.insert(2, ["wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn", "wpawn"])
	for x in range(2,6):
		board.insert(x, [ "", "", "", "", "", "", "", ""])
	board.insert(6, ["bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn", "bpawn"])
	board.insert(7, ["brook", "bknight", "bbishop", "bqueen", "bking", "bbishop", "bknight", "brook"])
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
		
