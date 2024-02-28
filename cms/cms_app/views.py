from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken 
from .serializers import UserSignupSerializer,UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

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
            token = get_token_for_user(user.email)
            response = Response({'msg':'Register Successful'},status=status.HTTP_201_CREATED)
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
                response = Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
                return response
            return Response({"errors":{"validation_erros":['password and email is not valid']}},status=status.HTTP_404_NOT_FOUND)
        
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token:
            RefreshToken(refresh_token).blacklist()
        
        response = Response({'msg': 'Logout Successful'}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh-token')
        response.delete_cookie('access-token')
        return response
        
class ContentItemView(APIView):
    def get(self,request,pk=None):
        
        
            

        
    


