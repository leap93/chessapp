from django.test import TestCase
from django.test.client import RequestFactory
from chessapp.models import Game, Move
from django.contrib.auth.models import User
from chessapp.views.games import games
from django.utils import timezone

class TestGames(TestCase):
	def setUp(self):
		self.factory = RequestFactory()
		self.cpu = User.objects.create_user(username='CPU', password='12345')
		self.user = User.objects.create_user(username='testuser', password='12345')
		self.bob = User.objects.create_user(username='bob', password='12345')
		login = self.client.login(username='testuser', password='12345')

	#page with no games
	def test_games_view_1(self):
		response = self.client.get('/chessapp/games')
		self.assertTrue("No games" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/games.html')
			
	#page with 4 games
	def test_games_view_2(self):
		game1 = Game.objects.create(start_date = timezone.now(), end_date = timezone.now(), black_player = self.user, white_player = self.cpu)
		game2 = Game.objects.create(start_date = timezone.now(), end_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		game3 = Game.objects.create(start_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		game4 = Game.objects.create(start_date = timezone.now(), black_player = self.user, white_player = self.cpu)
		response = self.client.get('/chessapp/games')
		self.assertTrue("No games" not in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/games.html')		

	#unknown game id
	def test_game_view_1(self):
		response = self.client.get('/chessapp/games?id=1000')
		self.assertTrue("Game ID is invalid" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/error.html')		

	#game where the player does not participate in
	def test_game_view_2(self):
		game = Game.objects.create(start_date = timezone.now(), white_player = self.bob, black_player = self.cpu)
		response = self.client.get('/chessapp/games?id=1')
		self.assertTrue("You are not participating in this game." in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/error.html')		

	#known game id
	def test_game_view_3(self):
		game = Game.objects.create(start_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		response = self.client.get('/chessapp/games?id=1')
		self.assertTrue("testuser against CPU" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/game.html')
	
	#execue illegal move
	def test_game_view_4(self):
		game = Game.objects.create(start_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		response = self.client.post('/chessapp/games?id=1', {"fromX": 0, "fromY": 0, "toX": 0, "toY": 4})
		self.assertTrue("Illegal move" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/game.html')		

	#execute legal move
	def test_game_view_5(self):
		game = Game.objects.create(start_date = timezone.now(), white_player = self.user, black_player = self.bob)
		response = self.client.post('/chessapp/games?id=1', {"fromX": 0, "fromY": 1, "toX": 0, "toY": 3})
		self.assertTrue("waiting" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/game.html')	
		