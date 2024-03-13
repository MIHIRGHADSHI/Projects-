from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    rest_owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1,)
    prod_code = models.IntegerField(default=100)
    added_by = models.CharField(max_length=50, default='user')
    item_name = models.CharField(max_length=50)
    item_desc = models.CharField(max_length=500, default='Dhoni finish off in style India lift the World Cup After 28 year party start in dressing room the indian captain icriduble')
    item_price = models.IntegerField()
    item_image = models.CharField(
        default = 'https://w7.pngwing.com/pngs/277/489/png-transparent-fast-food-eating-maps-location-placeholder-pin-icon.png',
        max_length=500
    )

    def __str__(self): 
        return self.item_name 


class History(models.Model):
    username = models.CharField(max_length=50, default='username')
    prod_code = models.IntegerField(default=100)
    item_name = models.CharField(max_length=50, default='itemname')
    operation_type = models.CharField(max_length=50, default='optyp')

    def __str__(self):
        return str(
            (
                self.username,
                self.prod_code,
                self.item_name,
                self.operation_type
            )

        )