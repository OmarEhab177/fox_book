from rest_framework import serializers

from users.models import CustomUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email',
            'fullname',
            'phone',
            'image',
            'code',
            'remember_token',
            'is_pan',
            'is_staff',
            'is_active',
            'date_joined',
            'updated_at',
        ]