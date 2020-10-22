from django.db import models


# Create your models here.
class Cart(models.Model):
    name = models.CharField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return self.name