from .import views
from django.urls import path

urlpatterns = [
    path('wards/', views.getWards, name = 'wards'),
    path('wastelist/', views.getWastes,name = 'wastes'),
    path('corporation/supervisorslist/', views.getSupervisors, name = 'supervisorslist'),
    path('corporation/collectionstatusupdate/', views.postCollectionStatusUpdate, name = 'collectionstatusupdate'),
    path('corporation/collectionstatus/', views.postCollectionStatus, name = 'collectionstatus'),
    path('corporation/collectorallocation/', views.postCollectorAllocation, name = 'collectorallocation'),
    path('corporation/employeelist/', views.Employee_details, name = 'excelupload'),
    path('corporation/wastereport/', views.postWasteReport, name = 'wastereport'),
    path('corporation/paymentreport/', views.getPaymentReport, name = 'paymentreport'),

    path('corporation/collectorlist/', views.postCollectorList, name = 'collectorlist'),
    path('corporation/editcollector/', views.updateCollector, name = 'editcollector'),
    path('corporation/addcollector/', views.postAddCollector, name = 'addcollector'),
    path('corporation/deletecollector/', views.postDeleteCollector, name = 'deletecollector'),

    path('corporation/editwaste/', views.updateWaste, name = 'editwaste'),
    path('corporation/addwaste/', views.postAddWaste, name = 'addwaste'),
    path('corporation/deletewaste/', views.postDeleteWaste, name = 'deletewaste'),

    path('corporation/supervisordetails/', views.getSupervisorList, name = 'supervisorslist'),
    path('corporation/editsupervisor/', views.updateSupervisor, name = 'editsupervisor'),
    path('corporation/addsupervisor/', views.postAddSupervisor, name = 'addsupervisor'),
    path('corporation/deletesupervisor/', views.postDeleteSupervisor, name = 'deletesupervisor'), 
]