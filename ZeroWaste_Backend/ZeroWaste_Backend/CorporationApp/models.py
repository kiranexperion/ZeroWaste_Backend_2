from django.db import models
# import HouseOwnerApp.models as ho_model

# Create your models here.
class wards(models.Model):

    wardno = models.CharField(max_length = 200, primary_key=True)
    wardname = models.CharField(max_length = 200)

class wastes(models.Model):

    waste_type = models.CharField(max_length = 200)
    charge = models.FloatField(max_length = None)

class roles(models.Model):

    rolename= models.CharField(max_length=30,unique=True)


class wastecollector(models.Model):

    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, unique=True, null=True)
    phoneno = models.CharField(max_length = 200, unique=True)
    address = models.CharField(max_length = 1000)
    wardno = models.ForeignKey(wards,on_delete=models.CASCADE)


class employee(models.Model):

    firstname = models.CharField(max_length = 200, null=True)
    lastname = models.CharField(max_length = 200, null=True)
    email = models.CharField(max_length = 200, unique=True)  
    phoneno = models.CharField(max_length = 200, null=True)
    address = models.CharField(max_length = 1000, null=True)
    designation = models.CharField(max_length=100,null = True)   
    role_id = models.ForeignKey(roles,on_delete=models.CASCADE)

class collectionstatus(models.Model):

    supervisor_id = models.ForeignKey(employee,on_delete=models.CASCADE)
    wardno = models.ForeignKey(wards,on_delete=models.CASCADE)
    status = models.CharField(max_length=200, default="Pending", null=True)
    collection_date = models.DateField(null=True)
    