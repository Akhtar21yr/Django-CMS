from rest_framework import serializers
from .models import CustomUser,ContentItem

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'password', 'password2', 'phone', 'address', 'city', 'state', 'country', 'pincode']

    def validate(self, data):
        if data['password'] != data['password2']:
             raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        return data

    def create(self, data):
        password = data.pop('password2', '')
        user = CustomUser.objects.create(**data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length = 255)
    class Meta:
        model = CustomUser
        fields = ['email','password']



class ContentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContentItem
        fields = ['title','body','summary']