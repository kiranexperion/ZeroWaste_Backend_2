from .import views
from django.urls import path

urlpatterns = [

    path('houseowner/signup/', views.postHouseOwner, name = 'signup'),
    path('houseowner/slotbooking/', views.postSlotBooking, name = 'slotbooking'),
    path('houseowner/bookinghistory/', views.getBookingHistory, name = 'bookinghistory'),
    path('houseowner/bookingstatus/', views.getBookingStatus, name = 'bookingstatus'),
    path('houseowner/invoice/', views.getBillGeneration, name = 'invoice'),
    path('houseowner/payment/', views.postPayment, name = 'payment'),
    path('houseowner/paymenthistory/',views.getPaymentHistory,name = 'paymenthistory'),
]