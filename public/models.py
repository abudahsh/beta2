from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    name=models.CharField(max_length=100)
    description= models.CharField(max_length=250)
    photo=models.ImageField()


    def __str__(self):
        return self.name


class ServiceProvider(models.Model):
    services=(
        ('a', 'Shopping'),
        ('b', 'Restaurant'),
        ('c', 'Automotive'),
        ('d', 'Cafe'),
        ('e', 'Gym & Spa'),
        ('f', 'Beauty'),
        ('g', 'Home Services'),
        ('g', 'Pets'),
        ('g', 'Others'),
    )
    creator=models.ForeignKey(User, related_name='services')
    name=models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    Phone=models.CharField(max_length=20, null=True, blank=True)
    photo=models.ImageField()
    review=models.PositiveSmallIntegerField(null=True)
    location=models.CharField(max_length=100)
    website=models.URLField(null=True)
    created_at=models.DateTimeField(auto_now_add=True)


    def get_absolute_url(self):
        return reverse('public:service_detail', kwargs={'pk':self.pk})

    def __str__(self):
        return self.name


class Product(models.Model):
    created_by=models.ForeignKey(ServiceProvider, related_name='products')
    name=models.CharField(max_length=150)
    description=models.TextField(max_length=500)
    photo=models.ImageField()
    price=models.PositiveSmallIntegerField(null=False)

    #def get_absolute_url(self):
    #    return reverse('public:product_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name+ ' ' +str(self.created_by)

class Review(models.Model):
    created_by=models.ForeignKey(User, related_name='reviews')
    body=models.TextField(max_length=500)
    rate=models.PositiveSmallIntegerField(null=True)
    review_of=models.ForeignKey(ServiceProvider, related_name='reviews', null=True, blank=True)
    product = models.ForeignKey(Product, related_name='reviews', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=False, auto_now=True)
    useful=models.PositiveSmallIntegerField(null=True, default=0)
    not_useful=models.PositiveSmallIntegerField(null=True, default=0)



    def __str__(self):
        return  'review for ' +str (self.product or self.review_of)