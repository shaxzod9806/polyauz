from django.db import models

# create a image source
images = '/static/players/images'


# Create your models here.
# na add ag tar
class Player(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    team = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    # address = models.ForeignKey(Addresses, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to=images, default='/static/players/images/default.jpg')

    def __str__(self):
        return self.name


class Addresses(models.Model):
    # country = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=50)

    # player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return self.street
