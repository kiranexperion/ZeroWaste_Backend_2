from rest_framework import serializers

from .models import houseowner
from .models import login
from .models import slotbooking
from .models import bookingstatus

class loginSerializer(serializers.ModelSerializer):
    class Meta:
        model = login
        fields = ['id','roleid','userid','email','password']
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def create(self,validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

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