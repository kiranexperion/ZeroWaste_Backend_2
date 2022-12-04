from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import houseowner
from .models import login
from .models import slotbooking

from .serializers import houseOwnerSerializer
from .serializers import slotBookingSerializer
from .serializers import bookingStatusSerializer
from .serializers import loginSerializer


import jwt, datetime
from django.db import connection


@api_view(['POST'])
def postHouseOwner(request):
    
    roleid = 1
    firstname = request.data['firstname']
    lastname = request.data['lastname']
    email = request.data['email']
    phoneno = request.data['phoneno']
    address = request.data['address']
    pincode = request.data['pincode']
    wardno = request.data['wardno']
    password = request.data['password']

    houseowner_data = {'firstname':firstname,'lastname':lastname,'email':email,'phoneno':phoneno,'address':address,'pincode':pincode,'wardno':wardno}

    serializer = houseOwnerSerializer(data = houseowner_data)

    if(serializer.is_valid()):
        serializer.save()
        login_data = {'roleid':roleid,'userid':serializer.data['id'],'email':email,'password':password}
        serializer_1 = loginSerializer(data = login_data)
        if(serializer_1.is_valid()):
            serializer_1.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postHouseOwnerlogin(request):
    data_email = request.data['email']
    data_password = request.data['password']

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
    response.data = {'jwt': token,'status':1}
    # response.headers = {'jwt': token}
    return response

@api_view(['POST'])
def postLogoutView(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {'message': 'Successfully logged out','status':1}
    return response

# @api_view(['GET'])
# def getUserView(request):
#     token = request.COOKIES.get('jwt')
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token,'secret',algorithms=['HS256'])
#     except jwt.ExpiredSignatureError :
#         raise AuthenticationFailed('Unauthenticated!')

#     user = houseowner.objects.filter(id = payload['id'])
#     serializer = houseOwnerSerializer(user,many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def postSlotBooking(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    
    ho_id = payload['id']
    waste_id = request.data['waste_id']
    booking_date = request.data['booking_date']
    quantity = request.data['quantity']

    data ={'houseowner_id':ho_id,'waste_id':waste_id,'quantity':quantity,'booking_date':booking_date}
   
    serializer = slotBookingSerializer(data = data)

    if(serializer.is_valid()):
        serializer.save()
        data_1 = {'booking_date':booking_date,'slot_id':serializer.data['id'],'status':'Pending'}
        serializer_1 = bookingStatusSerializer(data = data_1)
        if(serializer_1.is_valid()):
            serializer_1.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['GET'])
def getBookingHistory(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    ho_id = payload['id']

    cursor = connection.cursor()
    # cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_bookingstatus.collected_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.wastecollector_id from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status = %s",[ho_id,"collected"])
    cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_bookingstatus.collection_date,corporationapp_wastes.waste_type,corporationapp_employee.firstname,corporationapp_employee.lastname from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id inner join corporationapp_employee on houseownerapp_bookingstatus.supervisor_id_id = corporationapp_employee.id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status = %s",[ho_id,"Collected"])

    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}

        singleitem["bookingdate"]=item[0]
        singleitem["collectiondate"]=item[1]
        singleitem["wastetype"]=item[2]
        singleitem["supervisorname"]=item[3]+item[4]

        final_list.append(singleitem)

    return Response(final_list)

@api_view(['GET'])
def getBookingStatus(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    ho_id = payload['id']

    cursor = connection.cursor()
    cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_bookingstatus.collection_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.status,corporationapp_employee.firstname,corporationapp_employee.lastname from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id inner join corporationapp_employee on houseownerapp_bookingstatus.supervisor_id_id = corporationapp_employee.id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status != %s",[ho_id,"Collected"])

    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}

        singleitem["bookingdate"]=item[0]
        singleitem["collectiondate"]=item[1]
        singleitem["wastetype"]=item[2]
        singleitem["supervisorname"]=item[4]+item[5]
        singleitem["status"]=item[3]

        final_list.append(singleitem)

    return Response(final_list)
