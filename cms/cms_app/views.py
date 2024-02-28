from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken 
from .serializers import UserSignupSerializer,UserLoginSerializer,ContentItemSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser,ContentItem
from django.db.models import Q


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
    permission_classes = [IsAuthenticated]

    def search(self, request):
        user = request.user
        search_query = request.query_params.get('q', '')

        if user.is_admin:
            contents = ContentItem.objects.filter(
                Q(title__icontains=search_query) |
                Q(body__icontains=search_query) |
                Q(summary__icontains=search_query) |
                Q(categories__icontains=search_query)
            )
        else:
            contents = ContentItem.objects.filter(
                Q(author=user) &
                (Q(title__icontains=search_query) |
                 Q(body__icontains=search_query) |
                 Q(summary__icontains=search_query) |
                 Q(categories__icontains=search_query))
            )
        
        if contents:
            serializer = ContentItemSerializer(contents, many=True)
            return Response({'contents': serializer.data}, status=status.HTTP_200_OK)
        else :
            return Response({'msg':'no match data found'},status=status.HTTP_404_NOT_FOUND)

    def get(self,request,pk=None):
        if 'q' in request.query_params:
            return self.search(request)
        user = request.user
        if pk:
            try :
                content = ContentItem.objects.get(pk=pk)
            except :
                return Response({'msg':"content not found"},status=status.HTTP_404_NOT_FOUND)
            if not user.is_admin and content.author != user:
                return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
            serializer = ContentItemSerializer(content)
            return Response({'msg':serializer.data},status=status.HTTP_200_OK)
        else :
            if user.is_admin:
                contents = ContentItem.objects.all()
                print('---------------------.>>>>>>>>>>>>>>>>>>',user.is_admin)
            else :
                contents = ContentItem.objects.filter(author = user)
            if contents:
                serializer = ContentItemSerializer(contents,many=True)
                return Response({'contents':serializer.data},status=status.HTTP_200_OK)
            else :
                return Response({'msg':"user have not any content"},status=status.HTTP_404_NOT_FOUND)
        
    def post(self,request):
        user = request.user
        serializer = ContentItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['author' ] = user
            serializer.save()
            return Response({'msg':'Conten Created' , 'Content':serializer.data},status=status.HTTP_201_CREATED)
        else :
            print('--------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        user = request.user

        try:
            content = ContentItem.objects.get(pk=pk)
        except :
            return Response({'msg': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)
        
        if not user.is_admin and content.author != user:
            return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ContentItemSerializer(content, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Content updated', 'Content': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        user = request.user
        try:
            content = ContentItem.objects.get(pk=pk)
        except :
            return Response({'msg': 'Content not found'}, status=status.HTTP_404_NOT_FOUND)

        if not user.is_admin and content.author != user:
            return Response({'msg': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
        content.delete()
        return Response({'msg': 'Content deleted'}, status=status.HTTP_204_NO_CONTENT)
        
        
        
            

        
    


