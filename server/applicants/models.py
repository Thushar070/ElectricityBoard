from django.db import models

class Applicant(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15)
    address = models.TextField()
    meter_type = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.name
