from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from .product import Book


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + "'s cart"


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    if created:
        Cart.objects.create(user=instance)


class CartElement(models.Model):
    product = models.ForeignKey(Book, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.product) + ': ' + str(self.count)

    def increase(self, count):
        self.count += count
        self.save()



