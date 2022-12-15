from rest_framework import serializers

from .models import houseowner, slotbooking, bookingstatus, payment, paymentstatus

class houseOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = houseowner
        fields = ('__all__')

class slotBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = slotbooking
        fields = ('__all__')
    
class bookingStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = bookingstatus
        fields = ('__all__')

class paymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = payment
        fields = ('__all__')

class paymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = paymentstatus
        fields = ('__all__')
  