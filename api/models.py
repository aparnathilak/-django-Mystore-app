from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator  # to set min and max values


class Products(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to="images")

    @property  # to use the method as a property
    def avg_rating(self):  # self indicates an object of product
        ratings = self.reviews_set.all().values_list("rating", flat=True)
        if ratings:
            return sum(ratings)/len(ratings)
        else:
            return 0  # to avoid zero division error

    @property
    def review_user(self):
        ratings = self.reviews_set.all().values_list("rating", flat=True)
        if ratings:
            return len(ratings)
        else:
            return 0

    def __str__(self):
        return self.name


class Carts(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    options = (
        ("Order-placed", "Order-placed"),
        ("In-cart", "In-cart"),
        ("Cancelled", "Cancelled")
    )
    status = models.CharField(max_length=200, choices=options, default="In-cart")


class Reviews(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=200)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return self.review


class Orders(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    options = (
        ("Order-placed", "Order-placed"),
        ("Dispatched", "Dispatched"), 
        ("In-transit", "In-transit"),
        ("Cancelled", "Cancelled")
    )
    status = models.CharField(max_length=200, choices=options, default="Order-placed")
    date = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)

























# ORM(object relational mapping)
# ORM for creating resource

# modelname.objects.create(field1 = value1, field2=value2,-------) -> To insert values into table
# Products.object.create(name='Samsung', price=35000, category = 'electronics', description='mobile')


# django authentication and permissions
