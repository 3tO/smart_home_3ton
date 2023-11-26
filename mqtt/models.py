from django.db import models
from datetime import datetime


class Topic(models.Model):

    name = models.CharField(max_length=200, db_index=True, unique=True)

    def __str__ (self):
        return str(self.name)

class Values(models.Model):

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)
    date_pub = models.DateTimeField(default=datetime.now, db_index=True)

    