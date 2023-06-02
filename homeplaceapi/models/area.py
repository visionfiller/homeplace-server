from django.db import models

class Area(models.Model):
    neighborhood = models.CharField(max_length=100)
    city = models.ForeignKey("City",on_delete=models.CASCADE)
