from django.db import models
import hashlib, os

def HashPassword(passwd):
    passwd += '&^@#&(*~!+)^'
    return hashlib.sha256(passwd.encode()).hexdigest()

class User(models.Model):
    name = models.CharField(max_length=32)
    surname = models.CharField(max_length=32)
    login = models.CharField(max_length=32)
    mail = models.EmailField(max_length=64)
    passwd = models.CharField(max_length=256)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        ExtendedUser.objects.create(userID=self.id, ava="")

    def __str__(self):
        return "{} {} ({})".format(self.surname, self.name, self.login)

def getAvaName(instance, filename):
    ext = filename.split('.')[-1]
    filename = "{}_{}".format(instance.userID, filename)
    print(os.path.join(instance.standartAvaDir, filename))
    return os.path.join(instance.standartAvaDir, filename)

class ExtendedUser(models.Model):
    userID = models.IntegerField()
    ava = models.ImageField(upload_to=getAvaName)
    standartAvaDir = 'avatars/'

    def __str__(self):
        return self.userID

class Feedback(models.Model):
    user_id = models.IntegerField(default=0)
    title = models.CharField(max_length=32)
    text = models.CharField(max_length=1024)
    time = models.DateTimeField()

    def __str__(self):
        return self.title