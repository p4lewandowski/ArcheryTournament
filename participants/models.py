from django.db import models

# Create your models here.

class Participant(models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    points = models.IntegerField()

    def __str__(self):
        return self.name + " " + self.surname

    def as_json(self):
        return dict(
            name=self.name,
            surname=self.surname,
            points=self.points)
