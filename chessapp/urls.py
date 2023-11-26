from django.urls import path
from chessapp.views import index, registeration, login, games, new_game, logout

urlpatterns = [
    path("", index.index, name="index"),
	path("registeration", registeration.registeration, name="registeration"),
	path("login", login.login, name="login"),
	path("games", games.games, name="games"),
	path("new_game", new_game.new_game, name="new_game"),
	path("logout", logout.logoutpage, name="logout"),
	
]