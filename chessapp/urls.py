from django.urls import path
from chessapp.views import index, registeration, login, games

urlpatterns = [
    path("", index.index, name="index"),
	path("registeration", registeration.registeration, name="registeration"),
	path("login", login.login, name="login"),
	path("games", games.games, name="games"),
]