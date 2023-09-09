from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    country_code = models.CharField(max_length=50)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50)
    contact_picture = models.URLField(null=True, blank=True)
    is_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name}-{self.last_name}:{self.phone_number}"
