from rest_framework import serializers
from user.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if user is None:
            raise serializers.ValidationError("Invalid credentials")
        return user

class UpdateData(serializers.ModelSerializer):
    countGames = serializers.IntegerField(write_only=True)
    winGames = serializers.IntegerField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'countGames', 'winGames']

    def update(self, instance, validated_data):
        instance.countGames = validated_data.get('countGames', instance.countGames)
        instance.winGames = validated_data.get('winGames', instance.winGames)
        instance.save()
        return instance