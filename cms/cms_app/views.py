from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken 
from .serializers import UserSignupSerializer,UserLoginSerializer
from django.contrib.auth import authenticate

# Create your views here.

def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserSignupView(APIView):
    def post(self,request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = get_token_for_user(user)
            response = Response({'msg':'Register Successful'},status=status.HTTP_201_CREATED)
            response.set_cookie('token',token,httponly=True)
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class UserLoginView(APIView):
    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email,password=password)
            if user is not None :
                token = get_token_for_user(user)
                return Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
            return Response({"errors":{"non_field_erros":['password and email is not valid']}},status=status.HTTP_404_NOT_FOUND)
        
            

        
    


