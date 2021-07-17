from django.db import models
from django.core.validators import validate_slug, validate_email 



class userreg(models.Model):
    uname=models.CharField(max_length=100)
    pwd=models.CharField(max_length=100)
    email=models.EmailField()
    phone=models.CharField(max_length=100)
    vnumb=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    class Meta:
        db_table="login" 

class image(models.Model):

   
    ima=models.ImageField(upload_to="data")
    # ima_mime=models.CharField(max_length=100)
    ima_filename=models.CharField(max_length=100)
    ide=models.IntegerField()
    
    class Meta:
        db_table="image" 
class fineupl(models.Model):
    vnumber=models.CharField(max_length=100)
    cased=models.CharField(max_length=100)
    fineamt=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    class Meta:
        db_table="cases"
class transupl(models.Model):
    images=models.ImageField(upload_to="data")   
    vehicleno= models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    class Meta:
          db_table="transport"    