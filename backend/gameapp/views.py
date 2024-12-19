from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status
import json
from .models import Player, Game, User

@api_view(['POST'])
def createGame(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            game = Game.objects.create(status='newGame')
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)
