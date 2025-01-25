from django.db import models
from django.contrib.auth.models import User


class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number_of_rooms = models.FloatField(default=0.0)  # Changed to FloatField with default value
    number_of_bathrooms = models.FloatField(default=0.0)  # Changed to FloatField with default value
    number_of_floors = models.FloatField(default=0.0)  # Changed to FloatField with default value
    area = models.FloatField(default=0.0)  # Default value of 0.0
    road_width = models.FloatField(default=0.0)  # Default value of 0.0
    amenities_count = models.IntegerField(default=1)  # Default value of 1 for amenities_count
    city = models.CharField(max_length=255, default="")  # Default empty string for city
    road_type = models.CharField(max_length=255, default="")  # Default empty string for road_type
    predicted_price = models.FloatField(default=0.0)  # Default value of 0.0
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction by {self.user.username} on {self.prediction_date}"

