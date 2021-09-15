from django.contrib.auth.models import User
from django.db import models


class MessageWrapper(models.Model):
    text = models.CharField(max_length=255)
    sent_date = models.DateField()
    addressee = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

