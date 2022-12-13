from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed

from .models import houseowner, bookingstatus, slotbooking, payment, paymentstatus
from CorporationApp.models import wastes

from .serializers import houseOwnerSerializer, slotBookingSerializer, bookingStatusSerializer, paymentSerializer, paymentStatusSerializer
from LoginApp.serializers import loginSerializer
from .serializers import complaintsSerializer, complaintStatusSerializer

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

# @api_view(['POST'])
# def postHouseOwnerlogin(request):
#     data_email = request.data['email']
#     data_password = request.data['password']

#     user = login.objects.filter(email = data_email).first()

#     if user is None:
#         raise AuthenticationFailed('User not found')
#     if not user.check_password(data_password):
#         raise AuthenticationFailed('Incorrect password')
#     payload = {
#         'id':user.userid,
#         'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
#         'iat':datetime.datetime.utcnow()
#     }

#     token = jwt.encode(payload, 'secret',algorithm='HS256')
#     response =  Response()
#     response.set_cookie(key = 'jwt',value=token, httponly=True)
#     response.data = {'jwt': token,'status':1}
#     # response.headers = {'jwt': token}
#     return response

# @api_view(['POST'])
# def postLogoutView(request):
#     response = Response()
#     response.delete_cookie('jwt')
#     response.data = {'message': 'Successfully logged out','status':1}
#     return response

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
    # cursor.execute("SELECT houseownerapp_slotbooking.booking_date,houseownerapp_bookingstatus.collection_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.status,corporationapp_employee.firstname,corporationapp_employee.lastname from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id inner join corporationapp_employee on houseownerapp_bookingstatus.supervisor_id_id = corporationapp_employee.id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status != %s",[ho_id,"Collected"])
    cursor.execute("SELECT  houseownerapp_bookingstatus.id,houseownerapp_slotbooking.booking_date,houseownerapp_bookingstatus.collection_date,corporationapp_wastes.waste_type,houseownerapp_bookingstatus.status from houseownerapp_slotbooking inner join corporationapp_wastes on corporationapp_wastes.id = houseownerapp_slotbooking.waste_id_id inner join houseownerapp_bookingstatus on houseownerapp_slotbooking.id = houseownerapp_bookingstatus.slot_id_id where houseownerapp_slotbooking.houseowner_id_id = %s and houseownerapp_bookingstatus.status != %s",[ho_id,"Collected"])

    result = cursor.fetchall()

    final_list=[]

    for item in result:

        singleitem={}

        singleitem["bookingdate"]=item[1]
        singleitem["collectiondate"]= item[2]
        singleitem["wastetype"]=item[3]
        if item[2] is None:
            singleitem["supervisorname"]="NA"
        else:
            b_status = bookingstatus.objects.filter(id = item[0]).first()
            firstname = b_status.supervisor_id.firstname
            lastname = b_status.supervisor_id.lastname
            singleitem["supervisorname"]= firstname + " " + lastname
        singleitem["status"]=item[4]

        final_list.append(singleitem)

    return Response(final_list)


@api_view(['GET'])
def getBillGeneration(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    ho_id = payload['id']
    today = datetime.date.today()
    current_month = today.month
    user = paymentstatus.objects.filter(houseowner_id = ho_id).first()
    if user is not None:
        lastpay_month = user.last_paydate.month
    else:
        lastpay_month = None
    # grand_total = 0
    final_list=[]

    if current_month == lastpay_month:
        return Response({'message':'No Pending Bills'})
    else:
        # collected_slots = bookingstatus.objects.filter(status = 'Collected')
        # slots = slotbooking.objects.filter(id = collected_slots.slot_id.id, houseowner_id  = ho_id, payment_status = 0)
        slots = slotbooking.objects.filter(houseowner_id  = ho_id, payment_status = 0)

        waste_list = {}
        for slot in slots:
            # bookingstatus.slot_id.id = slot.id
            if slot.waste_id.waste_type not in waste_list:
                waste_list[slot.waste_id.waste_type] = slot.quantity
            else:
                waste_list[slot.waste_id.waste_type] = waste_list[slot.waste_id.waste_type] + slot.quantity
            slot.payment_status = 1
            slot.save()
        for i in waste_list:
            bill_item = {}
            waste = wastes.objects.filter(waste_type = i).first()
            unit_price = waste.charge
            total = waste_list[i] * unit_price
            bill_item['waste_type'] = i
            bill_item['quantity'] = waste_list[i]
            bill_item['unit_price'] = unit_price
            bill_item['total'] = total
            # grand_total = grand_total + total
            final_list.append(bill_item)
        return Response(final_list)
        # data = {'houseowner_id':ho_id,'totalamount':grand_total,'pay_date':today}
        # serializer = paymentSerializer(data = data)  
        # if(serializer.is_valid()):
        #     serializer.save()
        #     payments = paymentstatus.objects.filter(houseowner = ho_id).first()
        #     if payments is None:
        #         data_1 = {'houseowner':ho_id,'last_paydate':today}
        #         serializer_1 = paymentStatusSerializer(data=data_1)
        #         if(serializer_1.is_valid()):
        #             serializer_1.save()
        #     else:
        #         payments.last_paydate = today
        #         payments.save()
        

@api_view(['POST'])
def postPayment(request):
    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    ho_id = payload['id']
    paydate = request.data['paydate']
    grandtotal = request.data['grandtotal']
    status = request.data['status']

    if status is 1:
        data = {'houseowner_id':ho_id,'totalamount':grandtotal,'pay_date':paydate}
        serializer = paymentSerializer(data = data)  
        if(serializer.is_valid()):
            serializer.save()
            payments = paymentstatus.objects.filter(houseowner = ho_id).first()
            if payments is None:
                data_1 = {'houseowner':ho_id,'last_paydate':paydate}
                serializer_1 = paymentStatusSerializer(data=data_1)
                if(serializer_1.is_valid()):
                    serializer_1.save()
            else:
                payments.last_paydate = paydate
                payments.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['POST'])
def postComplaints(request):

    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError :
        raise AuthenticationFailed('Unauthenticated!')  

    ho_id = payload['id']
    subject = request.data['subject']
    description = request.data['description']
    registrationdate = request.data['registrationdate']
    issuedate = request.data['issuedate']  

    data ={'houseowner_id':ho_id,'subject':subject,'description':description,'registrationdate':registrationdate,'issuedate':issuedate}
    serializer = complaintsSerializer(data = data)

    if(serializer.is_valid()):
        serializer.save()
        data_1 = {'subject':subject,'description':description,'registrationdate':registrationdate,'complaints_id':serializer.data['id']}
        serializer_1 = complaintStatusSerializer(data = data_1)
        if(serializer_1.is_valid()):
            serializer_1.save()
        return Response({'status':1,'message':'Successfully Saved','data':serializer.data})
    else:
        return Response({'status':0,'message':'OOPS Some error occured','data':serializer.errors})

@api_view(['GET'])
def getcomplaintstatus(request):

    token = request.headers['Authorization']
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    try:
        payload = jwt.decode(token,'secret',algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
 
    cursor = connection.cursor()
    cursor.execute("SELECT houseownerapp_complaints.registrationdate,houseownerapp_complaints.subject,houseownerapp_complaints.description,houseownerapp_complaintstatus.remarks,houseownerapp_complaintstatus.status from houseownerapp_complaints inner join houseownerapp_complaintstatus on houseownerapp_complaints.id = houseownerapp_complaintstatus.complaints_id_id")
    result = cursor.fetchall()
    final_list=[]

    for item in result:
        singleitem={}
        singleitem["registrationdate"]=item[0]
        singleitem["subject"]=item[1]
        singleitem["description"]=item[2]
        singleitem["remarks"]=item[4]+item[5]
        singleitem["status"]=item[3]
        final_list.append(singleitem)

    return Response(final_list)