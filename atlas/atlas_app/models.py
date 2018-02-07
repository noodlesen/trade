from django.db import models

# Create your models here.


class Candle(models.Model):
    open_price=models.FloatField(null=True)
    high_price=models.FloatField(null=True)
    low_price=models.FloatField(null=True)
    close_price=models.FloatField(null=True)
    volume = models.IntegerField(null=True)
    symbol = models.CharField(max_length=15)
    timeframe = models.CharField(max_length=5)
    date = models.DateField(null=True)
    time = models.TimeField(null=True)
    provider = models.CharField(max_length=5)


class Instrument(models.Model):
    symbol = models.CharField(max_length=15)
            
