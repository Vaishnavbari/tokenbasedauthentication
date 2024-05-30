from rest_framework import serializers


class registration_user(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    email=serializers.EmailField()
    username=serializers.CharField()
    password=serializers.CharField()


class login_user(serializers.Serializer):
    email=serializers.EmailField()
    password=serializers.CharField()