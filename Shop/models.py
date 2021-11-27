from django.db import models
from django.contrib.auth import get_user_model


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    product_desc = models.CharField(max_length=256)
    price = models.IntegerField(default=-1)
    category = models.CharField(max_length=50, default="Any")
    subCategory = models.CharField(max_length=50, default="")
    Image = models.ImageField(upload_to="shop/images", default="")
    publish_date = models.DateField()
    rating = models.FloatField(default=4.0)

    def __str__(self):
        return self.product_name


class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=70, default="")
    email = models.CharField(max_length=70, default="")
    contactNo = models.IntegerField(default=-1)
    desc = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    amount = models.IntegerField(default=-1)
    name = models.CharField(max_length=128)
    email = models.CharField(max_length=128)
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default=-1)
    update_desc = models.CharField(default="", max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order_id)


User = get_user_model()


class Transaction(models.Model):
    made_by = models.ForeignKey(
        User, related_name='transactions', on_delete=models.CASCADE)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(
        unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_by and self.made_on:
            self.order_id = self.made_on.strftime(
                'PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)


class Ads(models.Model):
    adId = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="shop/images")
    adName = models.CharField(max_length=256, default="")
    adDesc = models.CharField(max_length=256, default="")
    pubDate = models.DateField(auto_now_add=True)
