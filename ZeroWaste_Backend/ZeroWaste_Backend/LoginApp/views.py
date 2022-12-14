from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

import jwt, datetime

from .models import login
from CorporationApp.models import employee
from .serializers import loginSerializer

@api_view(['POST'])
def postlogin(request):
    data_email = request.data['email']
    data_password = request.data['password']

    # FOR FIRST TIME LOGIN OF SUPERADMIN and ADMIN
    # emp = employee.objects.filter(email = data_email).first()
    # roleid = emp.role_id.id
    # userid = emp.id
    # data = {'roleid':roleid,'userid':userid,'email':data_email,'password':data_password}
    # serializer = loginSerializer(data = data)
    # if(serializer.is_valid()):
    #         serializer.save()
    # return Response(serializer.data)

    user = login.objects.filter(email = data_email).first()

    if user is None:
        raise AuthenticationFailed('User not found')
    if not user.check_password(data_password):
        raise AuthenticationFailed('Incorrect password')
    payload = {
        'id':user.userid,
        'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
        'iat':datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret',algorithm='HS256')
    response =  Response()
    response.set_cookie(key = 'jwt',value=token, httponly=True)
    response.data = {'jwt': token,'status':1,'role':user.roleid.id}
    return response
