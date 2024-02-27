from rest_framework import serializers
from .models import CustomUser

class UserSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password', 'password2', 'phone', 'address', 'city', 'state', 'country', 'pincode']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('Passwords do not match')
        
        return data

    def create(self, data):
        password = data.pop('password2', '')
        user = CustomUser.objects.create(**data)
        user.set_password(password)
        user.save()
        return user
