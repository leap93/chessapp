from django.test import TestCase
from django.test.client import RequestFactory
from chessapp.models import Game, Move
from django.contrib.auth.models import User
from chessapp.views.games import games
from django.utils import timezone

class TestGames(TestCase):
	def setUp(self):
		# Every test needs access to the request factory.
		self.factory = RequestFactory()
		self.cpu = User.objects.create_user(username='CPU', password='12345')
		self.user = User.objects.create_user(username='testuser', password='12345')
		login = self.client.login(username='testuser', password='12345')


	def test_games_view_1(self):
		response = self.client.get('/chessapp/games')
		self.assertEqual(response.status_code, 200)
		self.assertTrue("No games" in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/games.html')
		
	def test_games_view_2(self):
		game1 = Game.objects.create(start_date = timezone.now(), end_date = timezone.now(), black_player = self.user, white_player = self.cpu)
		game2 = Game.objects.create(start_date = timezone.now(), end_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		game3 = Game.objects.create(start_date = timezone.now(), white_player = self.user, black_player = self.cpu)
		game4 = Game.objects.create(start_date = timezone.now(), black_player = self.user, white_player = self.cpu)
		response = self.client.get('/chessapp/games')
		self.assertEqual(response.status_code, 200)
		self.assertTrue("No games" not in str(response.content))
		self.assertTemplateUsed(response, 'chessapp/games.html')		
		game1.delete()
		game2.delete()
		game3.delete()
		game4.delete()