from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound,AuthenticationFailed
from rest_framework.response import Response

from .models import wards
from .models import wastecollector
from .models import wastes
from .models import employee
from HouseOwnerApp.models import login
from HouseOwnerApp.models import bookingstatus
from .models import collectionstatus

from .serializers import wardsSerializer
from .serializers import wastesSerializer
from .serializers import wastecollectorSerializer
from .serializers import collectionstatusSerializer
from HouseOwnerApp.serializers import loginSerializer

import jwt, datetime
from django.db import connection


@api_view(['GET'])
def getWards(request):
    wardsList = wards.objects.all()
    serializer = wardsSerializer(wardsList, many = True)
    return Response(serializer.data)

@api_view(['GET'])
def getWastes(request):
    wasteList = wastes.objects.all()
    serializer = wastesSerializer(wasteList, many = True)
    return Response(serializer.data)

@api_view(['POST'])
def postCorporationlogin(request):
    data_email = request.data['email']
    data_password = request.data['password']

    # FOR FIRST TIME LOGIN
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
    response.data = {'jwt': token,'status':1,'role':user.roleid}
    return response

@api_view(['POST'])
def postCollectorList(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_wardno = request.data['wardno']
    list = wastecollector.objects.filter(wardno = data_wardno)
    
    if not list:
       return Response({'status':0})
    else:
        serializer = wastecollectorSerializer(list, many = True)
        return Response({'status':1,'data':serializer.data})

@api_view(['PUT'])
def updateCollector(request):

    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_id =request.data['id']
    data_email=request.data['email']
    data_phoneno=request.data['phoneno']
    data_address=request.data['address']
    collector = wastecollector.objects.filter(id = data_id).first()
    if collector is None:
        raise NotFound('Not found.')
    else:
        collector.email=data_email
        collector.phoneno=data_phoneno
        collector.address=data_address
        collector.save()
        serializer=wastecollectorSerializer(collector,many=False)
        return Response({'status':1,'data':serializer.data})

 

@api_view(['POST'])
def postAddCollector(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    serializer = wastecollectorSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postDeleteCollector(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_id=request.data['id']
    waste = wastecollector.objects.filter(id = data_id).delete()
    response = Response()
    if waste[0]==1:
        response.data = {'status':1,'message': 'Successfully deleted'}
        return response
    else:
        return Response({'status':0})

@api_view(['PUT'])
def updateWaste(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_id =request.data['id']
    data_charge=request.data['charge']
    waste = wastes.objects.filter(id = data_id).first()
    if waste is None:
        raise NotFound('Not found.')
    else:
        waste.charge=data_charge
        waste.save()
        serializer=wastesSerializer(waste,many=False)
        return Response({'status':1,'data':serializer.data})

@api_view(['POST'])
def postAddWaste(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    serializer = wastesSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postDeleteWaste(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_id=request.data['id']
    waste = wastes.objects.filter(id = data_id).delete()

    response = Response()
    if waste[0]==1:
        response.data = {'status':1,'message': 'Successfully deleted'}
        return response
    else:
        return Response({'status':0})

@api_view(['POST'])
def postCollectionStatusUpdate(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
    
    supervisor_id = payload['id']
    status = request.data['status']
    wardno = request.data['wardno']
    collection_date = request.data['collection_date']

    collection_status = collectionstatus.objects.filter(supervisor_id = supervisor_id, wardno = wardno, collection_date = collection_date).first()
    booking_status = bookingstatus.objects.filter(supervisor_id = supervisor_id, collection_date = collection_date)

    if collection_status is None:
        raise NotFound('Not found.')
    else:
        collection_status.status = status
        collection_status.save()
        for item in booking_status:
            item.status = status
            item.save()
        serializer = collectionstatusSerializer(collection_status,many = False)
        return Response({'status':1,'data':serializer.data})

@api_view(['POST'])
def postCollectionStatus(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    collection_date = request.data['collection_date']

    collection_status = collectionstatus.objects.filter(collection_date = collection_date)
 
    final_list=[]
    for item in collection_status:
        singleitem = {}
        singleitem["wardname"] = item.wardno.wardname
        singleitem["supervisor"] = item.supervisor_id.firstname + " " + item.supervisor_id.lastname
        singleitem["status"] = item.status

        final_list.append(singleitem)
    return Response(final_list)

@api_view(['POST'])
def postCollector(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')
