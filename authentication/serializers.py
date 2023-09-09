from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerailizer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    email = serializers.EmailField(max_length=255, min_length=4)
    first_name = serializers.CharField(max_length=255, min_length=2)
    last_name = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def validate(self, attrs):
        email = attrs.get("email", "")
        username = attrs.get("username", "")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {"email": ("Email already exists")})

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": ("user with that username already exists")})

        return super().validate(attrs)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=65, min_length=8, write_only=True)
    username = serializers.CharField(max_length=255, min_length=2)

    class Meta:
        model = User
        fields = ["username", "password"]
