from django.db import models

import CorporationApp.models as co_model

class houseowner(models.Model):
    
    firstname = models.CharField(max_length = 200)
    lastname = models.CharField(max_length = 200)
    email = models.CharField(max_length = 200, unique = True)
    phoneno = models.CharField(max_length = 200, unique =  True)
    address = models.CharField(max_length = 1000)
    pincode = models.CharField(max_length = 50)
    wardno = models.ForeignKey(co_model.wards, on_delete = models.CASCADE)

class slotbooking(models.Model):

    waste_id = models.ForeignKey(co_model.wastes, on_delete = models.CASCADE)
    houseowner_id = models.ForeignKey(houseowner, on_delete = models.CASCADE)
    booking_date = models.DateField(null = False)
    quantity = models.FloatField(null = False)
    payment_status = models.BooleanField(default = 0)

class bookingstatus(models.Model):

    slot_id = models.ForeignKey(slotbooking, on_delete = models.CASCADE)
    supervisor_id = models.ForeignKey(co_model.employee, null = True, on_delete = models.CASCADE)
    status = models.CharField(max_length = 200, default = "Pending")
    collection_date = models.DateField(null = True)
    booking_date = models.DateField(null = False)

class payment(models.Model):

    houseowner_id = models.ForeignKey(houseowner, on_delete = models.CASCADE)
    totalamount = models.FloatField()
    pay_date = models.DateField()

class paymentstatus(models.Model):

    houseowner = models.ForeignKey(houseowner, on_delete = models.CASCADE)
    last_paydate = models.DateField()
