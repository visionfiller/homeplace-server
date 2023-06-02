from django.db import models

class Rating(models.Model):
    swapper = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    property = models.ForeignKey("Property", on_delete=models.CASCADE, related_name="ratings")
    score = models.IntegerField()
    review = models.TextField(null=True, blank=True)
