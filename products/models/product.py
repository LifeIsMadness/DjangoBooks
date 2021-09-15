from django.db import models


class Product(models.Model):
    # code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    cost = models.FloatField()
    stock = models.IntegerField()
    image = models.CharField(max_length=100)
    # cart = models.ManyToManyField(Cart, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Book(Product):
    author = models.CharField(max_length=255, default='')
    page_count = models.IntegerField()
