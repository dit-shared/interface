from django.db import models
import hashlib

def HashPassword(passwd):
    passwd += '&^@#&(*~!+)^'
    return hashlib.sha256(passwd.encode()).hexdigest()

class User(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    mail = models.EmailField(max_length=64)
    passwd = models.CharField(max_length=256)

    def __str__(self):
        return self.surname + ' ' + self.name + ' (' + self.login + ')'

class Feedback(models.Model):
    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=32)
    text = models.CharField(max_length=1024)
    time = models.DateTimeField()

    def __str__(self):
        return self.title