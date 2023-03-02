from django.db import models

# Create your models here.
class Town(models.Model):
    id = models.AutoField(primary_key=True)
    code_postal = models.CharField(max_length=5)
    nom = models.CharField(max_length=254)

class Player(models.Model):
    email = models.EmailField(max_length=254, unique=True)
    lastname = models.CharField(max_length=254)
    firstname = models.CharField(max_length=254)
    password = models.CharField(max_length=50)
    idTown = models.ForeignKey(Town, on_delete=models.CASCADE)
    level = models.IntegerField(default=0)

    def __str__(self):
        return self.email

class Game(models.Model):
    idPlayer = models.ForeignKey(Player, on_delete=models.CASCADE)

class Verb(models.Model):
    id = models.AutoField(primary_key=True)
    base_verbale = models.CharField(max_length=50)
    participe_passe = models.CharField(max_length=50)
    preterit = models.CharField(max_length=50)
    traduction = models.CharField(max_length=254)

class Question(models.Model):
    idGame = models.ForeignKey(Game, on_delete=models.CASCADE)
    idVerb = models.ForeignKey(Verb, on_delete=models.CASCADE)
    answerPreterit = models.CharField(max_length=50)
    answerParticipePasse = models.CharField(max_length=50)
    dateIn = models.DateTimeField(auto_now_add=True)
