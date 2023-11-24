from django.db import models
from django.contrib.auth.models import User

class Confirmation(models.Model):
	user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE)
	confirmation_code = models.IntegerField(null=True)
	has_confirmed = models.BooleanField(default=False)

class Game(models.Model):
	white_player = models.ForeignKey(User, related_name="white", on_delete=models.CASCADE)
	black_player = models.ForeignKey(User, related_name="black", on_delete=models.CASCADE)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True)
	ended_by_forfeit = models.BooleanField(null=True, default=False)
	winner = models.ForeignKey(User, related_name="winner", on_delete=models.CASCADE, null=True)
	
class Move(models.Model):
	game = models.ForeignKey(Game, on_delete=models.CASCADE)
	move_date = models.DateTimeField()
	is_white = models.BooleanField()
	from_square = models.TextField()
	to_square = models.TextField()
	