from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound,AuthenticationFailed
from rest_framework.response import Response

from .models import wards
from .models import wastecollector
from .models import wastes

from .serializers import wardsSerializer
from .serializers import wastesSerializer
from .serializers import wastecollectorSerializer

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
def postCollectorList(request):

    data_wardno = request.data['wardno']
    list = wastecollector.objects.filter(wardno = data_wardno)
    
    if not list:
       return Response({'status':0})
    else:
        serializer = wastecollectorSerializer(list, many = True)
        return Response({'status':1,'data':serializer.data})

@api_view(['PUT'])
def updateCollector(request):

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

    serializer = wastecollectorSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postDeleteCollector(request):

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
    serializer = wastesSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postDeleteWaste(request):

    data_id=request.data['id']
    waste = wastes.objects.filter(id = data_id).delete()

    response = Response()
    if waste[0]==1:
        response.data = {'status':1,'message': 'Successfully deleted'}
        return response
    else:
        return Response({'status':0})