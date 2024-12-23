from django.http import JsonResponse
from django.template.defaultfilters import lower
from .serializers import UserSerializer, UserLoginSerializer, UpdateData
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import login
from user.models import User
import json
import requests
import threading


def createCometUser(data):
    username = data.get("username")
    # load_dotenv()
    # api_key = os.getenv("VUE_APP_COMMETCHAT_API_KEY")
    # comet_app_id = os.getenv("VUE_APP_COMMETCHAT_APP_ID")
    url = f"https://2683521c4e6c3899.api-eu.cometchat.io/v3/users"
    payload = {
        "avatar": "https://www.google.com/imgres?q=%D0%B0%D0%B2%D0%B0%D1%82%D0%B0%D1%80%D0%BA%D0%B0&imgurl=https%3A%2F%2Fillustrators.ru%2Fuploads%2Fillustration%2Fimage%2F1687137%2F14.jpg&imgrefurl=https%3A%2F%2Fillustrators.ru%2Fillustrations%2F1687137&docid=Ee9obntDZ71kfM&tbnid=zO2JN6AKL7PLYM&vet=12ahUKEwiCx_uH6quKAxU9KBAIHUnqO-kQM3oFCIYBEAA..i&w=2560&h=1600&hcb=2&ved=2ahUKEwiCx_uH6quKAxU9KBAIHUnqO-kQM3oFCIYBEAA",
        "uid": username,
        "name": username
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "apikey": "127bc8520b38325a216041848a7bba2eaaa850e0"
    }
    response = requests.post(url, json=payload, headers=headers)
    # print(api_key)
    # print(comet_app_id)
    print(response.text)


@api_view(['POST'])
def UserRegisterView(request):
    if request.method == 'POST':
        request.data['username'] = lower(request.data['username'])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            threading.Thread(target=createCometUser, args=(request.data,), daemon=True).start()
            # createCometUser(request.data)
            user = serializer.save()
            login(request, user)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    if request.method == 'POST':
        request.data['username'] = lower(request.data['username'])
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
        try:
            user = User.objects.get(username=username)
            responseData = {
                'countGames': user.countGames,
                'winGames': user.winGames,
            }
            print(responseData)
            return JsonResponse(responseData)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


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
                {"index": i + 1, "username": u.username, "winGames": u.maximumMoney}
                for i, u in enumerate(top_users)
            ]
            if user_position > 10:
                user_data.append({"index": user_position, "username": user.username, "winGames": user.maximumMoney})

            data = {"user_data" : user_data}

            return JsonResponse(data)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)