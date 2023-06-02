from django.db import models
from django.contrib.auth.models import User


class Swapper(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area = models.ForeignKey("Area", on_delete=models.CASCADE )
    favorites = models.ManyToManyField("Property", through="Favorite", related_name="swapper_favorites")

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def has_listing(self):
        return self.__has_listing
    @has_listing.setter
    def has_listing(self, value):
        self.__has_listing = value