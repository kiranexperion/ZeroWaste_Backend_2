from django.shortcuts import render

from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound,AuthenticationFailed
from rest_framework.response import Response

from .models import wards, wastecollector, wastes, employee, collectionstatus
from HouseOwnerApp.models import houseowner, slotbooking, bookingstatus, paymentstatus
from LoginApp.models import login

from .serializers import wardsSerializer, wastesSerializer, wastecollectorSerializer, collectionstatusSerializer, employeeSerializer
from LoginApp.serializers import loginSerializer

import jwt, datetime
from django.db import connection
import pandas as pd


'''
To get the list of wards
Developed by: KIRAN
'''
@api_view(['GET'])
def getWards(request):
    wardsList = wards.objects.all()
    serializer = wardsSerializer(wardsList, many = True)
    return Response(serializer.data)


'''
To get the list of wastes
Developed by: KIRAN
'''
@api_view(['GET'])
def getWastes(request):
    wasteList = wastes.objects.all()
    serializer = wastesSerializer(wasteList, many = True)
    return Response(serializer.data)


'''
To get the list of supervisors(id and name) - for dropdown
Developed by: KIRAN
'''
@api_view(['GET'])
def getSupervisors(request):
    supervisorsList = employee.objects.filter(role_id = 4)

    final_list=[]
    for item in supervisorsList:
        singleitem={}
        singleitem['id'] = item.id
        singleitem['name']= item.firstname + " " + item.lastname

        final_list.append(singleitem)

    return Response(final_list)


'''
Supervisor - Waste Collection Updation
Developed by: KIRAN
'''
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


'''
SuperAdmin/Admin - View the collection status based on a collection date
Developed by: KIRAN
'''
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


'''
SuperAdmin/Admin - Allot Supervisor and collection date for a ward after analysing the ward with highest quantity of wastes
Developed by: KIRAN
'''
@api_view(['POST'])
def postCollectorAllocation(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    wardno = request.data['wardno']
    supervisor_id = request.data['supervisor_id']
    collection_date = request.data['collection_date']
    status = request.data['status']

    data = {'status':status,'collection_date':collection_date,'supervisor_id':supervisor_id,'wardno':wardno}
    serializer = collectionstatusSerializer(data = data)
    if(serializer.is_valid()):
        serializer.save()

    x = bookingstatus.objects.all()
    for item in x:
        print(item.slot_id.houseowner_id.wardno)
        if(item.slot_id.houseowner_id.wardno.wardno == wardno):
            item.collection_date = collection_date
            item.supervisor_id = employee.objects.filter(id = supervisor_id).first()
            item.status = status
            item.save()
    return Response({'status':1})


'''
SuperAdmin/Admin - To upload Excel file containing details of contract employees(waste collectors)
Developed by: ARJUN
'''
@api_view(['POST'])
def Employee_details(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    if request.method == 'POST' and request.FILES['file']:     
        employeeexceldata = pd.read_excel(request.FILES['file'] )
        dbframe = employeeexceldata
        for dbframe in dbframe.itertuples():
            obj = wastecollector.objects.create(firstname=dbframe.firstname,lastname=dbframe.lastname,email=dbframe.email, phoneno=dbframe.phoneno, address=dbframe.address,wardno_id=dbframe.wardno_id,)
            obj.save()

    return Response({'message':'File Added Successfully'})


'''
SuperAdmin/Admin - To analyse the ward with highest quantity of waste before allocation
Developed by: KIRAN
'''
@api_view(['POST'])
def postWasteReport(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    wasteid = request.data['wasteid']

    slots = slotbooking.objects.filter(waste_id = wasteid)
    ward_quantity_list = {}
    for slot in slots:
            slot_status = bookingstatus.objects.filter(slot_id = slot.id).first()
            if slot_status.status != 'Collected':
                wardname = slot.houseowner_id.wardno.wardname
                if wardname not in ward_quantity_list:
                    ward_quantity_list[wardname] = slot.quantity
                else:
                    ward_quantity_list[wardname] = ward_quantity_list[wardname] + slot.quantity
    final_list = [ward_quantity_list]
    return Response(final_list)


'''
SuperAdmin/Admin - To view the list of houseowners whose payment is pending and also those who have completed the payment
Developed by: ARJUN
'''
@api_view(['GET'])
def getPaymentReport(request):

    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!') 

    payments_status = paymentstatus.objects.all()
    today = datetime.date.today()
    current_month = today.month      
    final_list=[]

    for item in payments_status:
        ho_id = item.houseowner
        lastpay_month = item.last_paydate.month
        singleitem = {}
        singleitem["firstname"] = ho_id.firstname
        singleitem["last"] = ho_id.lastname
        singleitem["phoneno"] = ho_id.phoneno
        singleitem["address"] = ho_id.address
        singleitem["wardname"] = ho_id.wardno.wardname

        if current_month == lastpay_month:    
            singleitem["status"] = 'Paid'
        else:
            singleitem["status"] = 'Pending'
        final_list.append(singleitem)

    return Response(final_list)


'''
SuperAdmin/Admin - To display the list of contract employees(waste collectors) based on ward
Developed by: ARJUN
'''
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


'''
SuperAdmin/Admin - To edit the details of a contract employee(waste collector)
Developed by: ARJUN
'''
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

 
'''
SuperAdmin/Admin - To add a new contract employee(waste collector)
Developed by: ARJUN
'''
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


'''
SuperAdmin/Admin - Delete contract employee(waste collector)
Developed by: ARJUN
'''
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


'''
SuperAdmin - To edit the details of waste
Developed by: ARJUN
'''
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


'''
SuperAdmin - To add a new waste type and its details
Developed by: ARJUN
'''
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


'''
SuperAdmin - Delete Waste
Developed by: ARJUN
'''
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


'''
SuperAdmin/Admin - To get the list of supervisors(contains all details of a supervisor)
Developed by: ARJUN
'''
@api_view(['GET'])
def getSupervisorList(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    supervisorList = employee.objects.filter(roleid = 4)
    
    if not supervisorList:
       return Response({'status':0})
    else:
        serializer = employeeSerializer(supervisorList, many = True)
        return Response({'status':1,'data':serializer.data})


'''
SuperAdmin/Admin - To edit the details of a supervisor
Developed by: ARJUN
'''
@api_view(['PUT'])
def updateSupervisor(request):

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
    supervisor = employee.objects.filter(id = data_id).first()
    if supervisor is None:
        raise NotFound('Not found.')
    else:
        supervisor.email=data_email
        supervisor.phoneno=data_phoneno
        supervisor.address=data_address
        supervisor.save()
        serializer = employeeSerializer(supervisor,many=False)
        return Response({'status':1,'data':serializer.data})

 
'''
SuperAdmin/Admin - To add a new supervisor
Developed by: ARJUN
'''
@api_view(['POST'])
def postAddSupervisor(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_email = request.data['email']
    data_password = 'supervisor@123'

    serializer = employeeSerializer(data = request.data)
    if(serializer.is_valid()):
        serializer.save()
        login_data = {'roleid':4, 'userid':serializer.data['id'],'email':data_email,'password':data_password}
        serializer_1 = loginSerializer(data = login_data)
        if(serializer_1.is_valid()):
            serializer_1.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})


'''
SuperAdmin/Admin - Delete supervisor
Developed by: ARJUN
'''
@api_view(['POST'])
def postDeleteSupervisor(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')

    data_id=request.data['id']
    supervisor = employee.objects.filter(id = data_id).delete()
    response = Response()
    if supervisor[0]==1:
        response.data = {'status':1,'message': 'Successfully deleted'}
        return response
    else:

        return Response({'status':0})




                  
