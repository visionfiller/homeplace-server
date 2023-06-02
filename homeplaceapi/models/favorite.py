from django.db import models


class Favorite(models.Model):
    swapper = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    property = models.ForeignKey("Property", on_delete=models.CASCADE)
   