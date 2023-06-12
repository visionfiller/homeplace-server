from django.db import models



class Property(models.Model):

    owner = models.ForeignKey("Swapper", on_delete=models.CASCADE)
    area = models.ForeignKey("Area", on_delete=models.CASCADE )
    property_type = models.ForeignKey("PropertyType", on_delete=models.CASCADE, null=True, blank=True)
    bedrooms = models.IntegerField(null=True, blank=True)
    bathrooms = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    yard = models.BooleanField()
    pool = models.BooleanField()
    square_footage = models.IntegerField()

 
    @property
    def user_favorited(self):
        return self.__user_favorited
    @user_favorited.setter
    def user_favorited(self, value):
        self.__user_favorited = value
    @property
    def average_rating(self):
        """Average rating calculated attribute for each product
        Returns:
            number -- The average rating for the product
        """
       
        try:
            ratings = self.ratings.all()
            total_rating = 0
            for rating in ratings:
                total_rating += rating.score

            avg = total_rating / self.ratings.count()
            return avg
        except ratings.DoesNotExist:
            total_rating=0
            avg = total_rating
            return avg