from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    osm_id = models.CharField(max_length=255, unique=True)  # OSM identifier
    def __str__(self):
        return self.name

