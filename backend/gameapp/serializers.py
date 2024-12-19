# from rest_framework import serializers
# from .models import Game, Player
# from django.contrib.auth import authenticate
#
# class UserSerializer(serializers.ModelSerializer):
#     status = serializers.CharField(max_length=50)
#
#     class Meta:
#         model = Game
#         fields = ['status']
#
#     def create(self, validated_data):
#         user = User.objects.create_user(**validated_data)
#         return user