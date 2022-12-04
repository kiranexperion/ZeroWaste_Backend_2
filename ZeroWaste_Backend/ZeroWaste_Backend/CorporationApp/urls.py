from .import views
from django.urls import path

urlpatterns = [
    path('wards/',views.getWards, name='wards'),
    path('wastelist/',views.getWastes,name = 'wastes'),
    path('corporation/collectorlist/', views.postCollectorList, name='collectorlist'),
    path('corporation/editcollector/',views.updateCollector,name='editcollector'),
    path('corporation/addcollector/',views.postAddCollector,name='addcollector'),
    path('corporation/deletecollector/',views.postDeleteCollector,name='deletecollector'),
    path('corporation/editwaste/',views.updateWaste,name='editwaste'),
    path('corporation/addwaste/',views.postAddWaste,name='addwaste'),
    path('corporation/deletewaste/',views.postDeleteWaste,name='deletewaste'),
]