from django.db import models
import HouseOwnerApp.models as ho_model

# Create your models here.
class wastes(models.Model):

    waste_type = models.CharField(max_length = 200, null = False)
    charge = models.FloatField(max_length = None,null = False)

class roles(models.Model):

    rolename= models.CharField(max_length=30,unique=True)


class wastecollector(models.Model):

    name= models.CharField(max_length=100,null = False)   
    phoneno = models.CharField(max_length = 200, unique=True)
    address = models.CharField(max_length = 1000)
    wardno = models.BigIntegerField()


class employee(models.Model):

    name= models.CharField(max_length=100,null = False)   
    phoneno = models.CharField(max_length = 200)
    address = models.CharField(max_length = 1000)
    designation = models.CharField(max_length=100,null = False)   
    role_id = models.ForeignKey(roles,on_delete=models.CASCADE)

class collectionstatus(models.Model):

    supervisor_id = models.ForeignKey(employee,on_delete=models.CASCADE)
    wardno = models.BigIntegerField()
    status = models.CharField(max_length=200, default="Pending")
    
