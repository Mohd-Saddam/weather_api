from django.db import models

# Create your models here.
class CityModel(models.Model):
    city = models.CharField( max_length=20 )

    class Meta:
        verbose_name_plural = "Cities"

    
    def __str__(self):
        return self.city