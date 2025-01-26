from django.http import JsonResponse
from django.template.defaultfilters import random
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import json
from .models import Player, Game, User, Question, Answer, Chance, Professions, Action

@api_view(['POST'])
def createGame(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            profession = Professions.objects.order_by('?').first()
            player.profession = profession
            player.balance = profession.salary
            player.save()
            game = Game.objects.create(status='newGame')
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def createPlayer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            game = Game.objects.get(id=data['id'])
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User or game not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def changePlayer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            player = Player.objects.get(id=data['player_id'])
            if data['profession']:
                profession = Professions.objects.get(id = data['profession'])
                player.profession = profession
                player.save()
            return JsonResponse({'playerID': player.id, 'balance': player.balance, 'profession': player.profession})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def addActionAnswer(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            player = Player.objects.get(id=data['player_id'])
            answer = Answer.objects.get(id=data['answer_id'])
            player.balance -= answer.sum_now
            if answer.sum_later or answer.scip:
                action = Action.objects.create(player=player, sum=answer.sum_later, period=answer.period, scip = answer.scip)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def addActionChance(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        player_id = data.get('player_id')
        chance_id = data.get('chance_id')
        if not player_id or not chance_id:
            return Response(
                {"detail": "player_id and chance_id are required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            player = Player.objects.get(id=player_id)
            chance = Chance.objects.get(id=chance_id)
            if chance.period or chance.scip:
                action = Action.objects.create(player=player, sum=chance.sum, period=chance.period, scip = chance.scip)
                return Response({"action_id": action.id, "balance": player.balance}, status=status.HTTP_201_CREATED)
            if chance.period == 0:
                player.balance += chance.sum
                player.save()
                return JsonResponse({"balance": player.balance})
            return Response({"detail": "Action created", "balance": player.balance}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def checkScip(request):
    if request.method == 'POST':
        player_id = request.data.get('player_id', None)
        if not player_id:
            return Response({"detail": "player_id is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            player = Player.objects.get(id=player_id)
            actions = Action.objects.filter(player=player, scip=True)
            if not actions:
                return JsonResponse({'scip': False})
            for action in actions:
                action.scip = False
                action.save()
            return JsonResponse({'scip': True})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def changeBalance(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            player = Player.objects.get(id=data['player_id'])
            player.balance += player.profession.salary
            actions = Action.objects.filter(player=player)
            income = 0
            outcome = 0
            for action in actions:
                if action.period > 0:
                    player.balance += action.sum
                    action.period -= 1
                    action.save()
                    if action.sum > 0:
                        income += action.sum
                    else:
                        outcome -= action.sum
            player.save()
            return JsonResponse({'balance': player.balance, 'salary': player.profession.salary, 'income': income, 'outcome': outcome})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


api_view(['GET'])
def getQuestion(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        try:
            question = Question.objects.get(id=id)
            responseData = {
                "category": question.category,
                "text": question.text,
                "type": question.type
            }
            return JsonResponse(responseData)
        except Question.DoesNotExist:
            return Response({"detail": "Question not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['Get'])
def getAnswers(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        if not id:
            return Response({"detail": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answers = Answer.objects.filter(question=id)
            responseData = []
            for answer in answers:
                responseData.append({
                    "id": answer.id,
                    "text": answer.answer_text
                })
            return JsonResponse(responseData, safe=False)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def getAnswerOutcome(request):
    if request.method == 'GET':
        answer_id = request.GET.get('answer_id', None)
        if not answer_id:
            return Response({"detail": "Parameter 'id' is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            answer = Answer.objects.get(id=answer_id)
            outcome = answer.action_text
            return JsonResponse({"outcome": outcome})
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['Get'])
def getRandomQuestion(request):
    if request.method == 'GET':
        category_id = request.GET.get('category_id', None)
        try:
            question = Question.objects.filter(category=category_id).order_by('?').first()
            responseData = {
                "id" : question.id,
                "category": question.category,
                # "text": question.text,
                "type": question.type
            }
            return JsonResponse(responseData)
        except Question.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
def connectToGame(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode())
        try:
            user = User.objects.get(username=data['username'])
            player = Player.objects.create(user=user)
            profession = Professions.objects.order_by('?').first()
            player.profession = profession
            player.balance = profession.salary
            player.save()
            game = Game.objects.get(id=data["game_id"])
            game.players.add(player)
            return JsonResponse({'gameId': game.id, 'playerID': player.id})
        except User.DoesNotExist:
            return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getInfoAboutGame(request):
     if request.method == 'GET':
         game_id = request.GET.get('gameId', None)
         try:
             game = Game.objects.get(id=game_id)
             players = list(game.players.all())
             return JsonResponse({'players': [
                     {
                        'id': player.id,
                        'name': player.user.username,
                        'profession': player.profession.name,
                        'balance': player.balance,
                        'salary': player.profession.salary
                     } for player in players
                ]
             })
         except Game.DoesNotExist:
             return JsonResponse({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['Get'])
def getRandomChance(request):
    if request.method == 'GET':
        try:
            chance = Chance.objects.order_by('?').first()
            responseData = {
                "id" : chance.id,
                # "text": chance.text,
            }
            return JsonResponse(responseData)
        except Chance.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['Get'])
def getChance(request):
    if request.method == 'GET':
        id = request.GET.get('id', None)
        try:
            chance = Chance.objects.get(id=id)
            responseData = {
                # "category": chance.category,
                "text": chance.text
            }
            return JsonResponse(responseData)
        except Chance.DoesNotExist:
            return Response({"detail": "Chance not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['Get'])
def getRandomProfession(request):
    if request.method == 'GET':
        player_id = request.GET.get('player_id', None)
        try:
            profession = Professions.objects.order_by('?').first()
            player = Player.objects.get(id=player_id)
            if not player.profession:
                player.profession = profession
                player.save()
                responseData = {
                    "id" : profession.id,
                    "name": profession.name,
                    "salary": profession.salary,
                }
                return JsonResponse(responseData)
            return JsonResponse({"detail": "player already has profession"})
        except Professions.DoesNotExist:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def getActiveGames(request):
    if request.method == 'GET':
        print(1234567890)
        try:
            games = [game for game in Game.objects.filter(status='newGame')]
            responseData = [{
                'game_id': game.id,
                'username': game.players.first().user.username if game.players.exists() else None,
            } for game in games]
            return JsonResponse(responseData, safe=False)
        except Exception as e:
            return Response(
                {"detail": f"An error occurred: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
