from .import views
from django.urls import path

urlpatterns = [

    path('houseowner/signup/',views.postHouseOwner,name = 'signup'),
    # path('houseowner/login/',views.postHouseOwnerlogin,name = 'login'),
    # path('houseowner/logout/',views.postLogoutView,name = 'logout'),
    path('houseowner/slotbooking/',views.postSlotBooking, name='slotbooking'),
    path('houseowner/bookinghistory/',views.getBookingHistory, name='bookinghistory'),
    path('houseowner/bookingstatus/',views.getBookingStatus, name='bookingstatus'),
    path('houseowner/invoice/',views.getBillGeneration,name = 'invoice'),
    path('houseowner/payment/',views.postPayment,name = 'payment'),
    path('houseownerapp/complaints/',views.postComplaints,name = 'complaints'),
    path('houseownerapp/complaintstatus/',views.getcomplaintstatus,name = 'complaintstatus'),
]