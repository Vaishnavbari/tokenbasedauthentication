from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import user_registration

class custom_authentication(BasePermission):
    
    def has_permission(self, request, view):
        if request.method == 'PUT':
            auth_header=request.headers.get("Authorization")
            if not auth_header:
                return
            user=Token.objects.filter(key=auth_header).first()
            if not user:
                return Response({"msg":"user is not valid"})
            else:
                user = user_registration.objects.filter(email=user.user_id.email)

                return user is not None
            
                  
        # return super().has_permission(request, view)