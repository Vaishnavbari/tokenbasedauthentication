from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import user_registration

class custom_autherization(BasePermission):

    def authenticate(self, request):
    
        auth_header=request.headers.get("Authorization")

        if not auth_header:
            return Response({"msg":"please provide authentication token"})
        
        token = auth_header.split(' ')[-1]

        user_token=Token.objects.filter(key=token).first()
        user = user_registration.objects.filter(email=user_token.user.email).first()
        
        print(">>>>>>>>>>>>>>",user)
        if not user:
            return user is None
        else:
            return user
     
    
    def has_permission(self, request, view):
        user = self.authenticate(request)
        request.user=user
        return True

       
            
                  
        # return super().has_permission(request, view)