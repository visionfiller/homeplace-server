from django.db import models



class Property(models.Model):

    owner = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    area = models.ForeignKey("Area", on_delete=models.CASCADE )
    address = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    yard = models.BooleanField()
    square_footage = models.IntegerField()
 
    @property
    def user_favorited(self):
        return self.__user_favorited
    # TODO: Add a `is_favorite` custom property. Remember each JSON representation of a restaurant should have a `is_favorite` property. Not just the ones where the value is `true`.
    @user_favorited.setter
    def user_favorited(self, value):
        self.__user_favorited = value