from django.db import models


class PaymentType(models.Model):

    swapper = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    acct_number= models.IntegerField()
    merchant_name = models.CharField(max_length=25)