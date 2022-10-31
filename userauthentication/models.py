from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    firstName = models.CharField(max_length=20)
    lastName = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    email =  models.EmailField(max_length=100, unique= True)
    address = models.CharField(max_length= 250)
    password = models.CharField(max_length=255)
    phoneNumber = models.CharField(max_length=15)
    username = None
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS =['firstName', 'password', 'lastName', 'address' ]




