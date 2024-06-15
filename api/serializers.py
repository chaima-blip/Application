from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }
        

        def create(self, validated_data):
        # Ensure email uniqueness check
            email = validated_data['email']
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError("Email already exists.")
            
            # Create user
            user = User.objects.create_user(**validated_data)
            return user
