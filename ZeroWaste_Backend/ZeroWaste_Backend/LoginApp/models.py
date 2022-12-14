from django.db import models
from django.contrib.auth.models import AbstractUser

import CorporationApp.models as co_model

class login(AbstractUser):

    username = None
    first_name = None
    last_name = None
    is_staff = None
    is_active = None
    is_superuser = None

    roleid = models.ForeignKey(co_model.roles, on_delete = models.CASCADE)
    userid = models.BigIntegerField(null = False)
    email = models.CharField(max_length = 200, unique = True)
    password = models.CharField(max_length = 200)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []