from rest_framework import generics, status
from rest_framework.response import Response
import requests
from rest_framework.views import APIView

from vk_telegram.models import MessageOnWall
from vk_telegram.serializers import MessageOnWallSerializer


def send_to_telegram(text: str):
    """Send message to telegram chat"""
    token = "xxxxxxx"
    url = "https://api.telegram.org/bot"
    channel_id = "-0000000"
    url += token
    url += "/sendMessage"

    r = requests.post(url, data={
         "chat_id": channel_id,
         "text": text
          })

    return r.status_code


def get_username_from_vk(user_vk_id):
    """Get user full name from VK"""
    token = 'xxxxxx'
    v = '5.131'
    r = requests.get(
        f'https://api.vk.com/method/users.get?user_ids={user_vk_id}&fields=bdate&access_token={token}&v={v}')

    if r.status_code != 200:
        return r.status_code

    json = r.json()
    user_full_name = json['response']['first_name'] + json['response']['last_name']
    return user_full_name


class CreateView(APIView):

    def post(self, request):
        if request.data['type'] not in ['wall_post_new', 'wall_repost']:
            Response(status=status.HTTP_400_BAD_REQUEST)
        user_vk_id = request.data['object']['user_id']
        message = request.data['object']['text']
        data = request.data
        data['message'] = message

        user_full_name = get_username_from_vk(user_vk_id)
        if isinstance(user_full_name, int):
            Response(status=status.HTTP_400_BAD_REQUEST)

        data['user_name'] = user_full_name

        serializer = MessageOnWallSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

        text = f'Пишет новый пользователь {user_full_name}: {message}'

        if send_to_telegram(text) != 200:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListView(generics.ListAPIView):
    queryset = MessageOnWall.objects.all()
    serializer_class = MessageOnWallSerializer
