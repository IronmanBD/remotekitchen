from rest_framework import serializers
from .models import Account


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True, required= False)

    class Meta:
        model = Account
        fields = ['id', 'username', 'email', 'role', 'is_active', 'date_joined', 'password']
        read_only_fields = ['id', 'is_active', 'date_joined']

    def create(self, validated_data):
        user = Account.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                password=validated_data['password'],
                role=validated_data['role']
        )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()