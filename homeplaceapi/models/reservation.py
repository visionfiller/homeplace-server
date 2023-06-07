from django.db import models


class Reservation(models.Model):

    swapper = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    property = models.ForeignKey("Property", on_delete=models.CASCADE )
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=15, default=False)
    completed = models.BooleanField(default=False)

   