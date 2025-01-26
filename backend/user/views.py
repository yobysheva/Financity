from django.http import JsonResponse
from django.template.defaultfilters import lower
from .serializers import UserSerializer, UserLoginSerializer, UpdateData, UpdatePhoto
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from user.models import User
import json
import requests
import threading


@api_view(['POST'])
def UserRegisterView(request):
    if request.method == 'POST':
#         request.data['username'] = lower(request.data['username'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # threading.Thread(target=createCometUser, args=(request.data,), daemon=True).start()
            # createCometUser(request.data)
            user = serializer.save()
            login(request, user)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
#         request.data['username'] = lower(request.data['username'])
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_202_ACCEPTED)
        print(serializer.errors)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


api_view(['Get'])
def getData(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        users =  User.objects.all().order_by('-winGames')
        user = User.objects.get(username=username)
        user_position = list(users).index(user) + 1
        try:
            responseData = {
                'countGames': user.countGames,
                'winGames': user.winGames,
                'indexPhoto': user.indexPhoto,
                'place': user_position,
            }
            return JsonResponse(responseData)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def updatePhoto(request):
    if request.method == "PUT":
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdatePhoto(instance=user, data=data)

        if serializer.is_valid():
            update_user = serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


api_view(['PUT'])
def updateData(request):
    if request.method == 'PUT':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateData(instance=user, data=data)

        if serializer.is_valid():
            update_user = serializer.save()
            return JsonResponse(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


api_view(['GET'])
def getStats(request):
    if request.method == 'GET':
        username = request.GET.get('username', None)
        try:
            users =  User.objects.all().order_by('-winGames')
            user = User.objects.get(username=username)
            user_position = list(users).index(user) + 1
            top_users = users[:10]
            user_data = [
                {"index": i + 1, "username": u.username, "winGames": u.winGames, "countGames": u.countGames}
                for i, u in enumerate(top_users)
            ]
            if user_position > 10:
                user_data.append({"index": user_position,
                                  "username": user.username,
                                  "winGames": user.winGames,
                                  "countGames": user.countGames,
                                  "indexPhoto": user.indexPhoto})

            data = {"user_data" : user_data}

            return JsonResponse(data)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)