from django.shortcuts import render
from .models import user_registration 
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login  as auth_login,logout
from rest_framework.authtoken.models import Token
from app.app_serializer import registration_user,login_user
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.csrf import csrf_exempt
from .token_authoeization import custom_authentication
from rest_framework.authentication import TokenAuthentication,SessionAuthentication,BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@method_decorator(csrf_exempt,name='post')
class registration(APIView):

    authentication_classes=[TokenAuthentication]

    
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def post(self,request):

        serializer=registration_user(data=request.data)

        if serializer.is_valid():
            first_name=serializer.validated_data.get("first_name")
            last_name=serializer.validated_data.get("last_name")
            email=serializer.validated_data.get("email")
            username=serializer.validated_data.get("username")
            password=serializer.validated_data.get("password")

            if user_registration.objects.filter(username=username).exists():
                return Response({"message":"username alleady exist "},status=400)
            elif user_registration.objects.filter(email=email).exists():
                return Response({"message":"email alleady exist "},status=400)

            user=user_registration.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,password=make_password(password))
            
            # Genrate the token

            token=Token.objects.create(user=user)

            return Response({"message":"user registered sucessfully ","token":token.key},status=200)
        
        return Response({"message":"Something went wrong"},status=500)



class login(APIView):

    authentication_classes=[TokenAuthentication]

    def post(self,request):
        
        serializer = login_user(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            password = serializer.validated_data.get("password")
            
            user = authenticate(request,email=email,password=password)

            if user :

                auth_login(request,user)
                
                return Response({"message":"user login sucessfully "},status=200)
            else:
                return Response({"message":"inavalid user"},status=200)

        return Response(serializer.errors, status=400)
    

@method_decorator(csrf_exempt,name="dispatch")
class update_user(APIView):

    authentication_classes=[BasicAuthentication]
    permission_classes=[custom_authentication]

        
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def put(self,request,id):

        if id is not None:

            serializer=registration_user(data=request.data,partial=True)
            user=user_registration.objects.filter(id=id).first()
            
            if serializer.is_valid():
                user.first_name=serializer.validated_data.get("first_name",user.first_name)
                user.email=serializer.validated_data.get("email",user.email)
                if serializer.validated_data.get("password"):
                   user.password=make_password(serializer.validated_data.get("password"))
                user.password=user.password
                user.last_name=serializer.validated_data.get("last_name",user.last_name)
                user.save()
                return Response({"message":"user updated sucessfully "},status=200)

            return Response(serializer.errors, status=400)


