from rest_framework import generics, status
from rest_framework.response import Response
import requests
from rest_framework.views import APIView

from vk_telegram.models import MessageOnWall
from vk_telegram.serializers import MessageOnWallSerializer


def send_to_telegram(text: str):
    token = "2138321296:AAE3D6WoofLImmgCEPn1-6n9YXuokr1QJ4c"
    url = "https://api.telegram.org/bot"
    channel_id = "-1001703747250"
    url += token
    url += "/sendMessage"

    r = requests.post(url, data={
         "chat_id": channel_id,
         "text": text
          })

    return r


def get_username_from_vk(user_vk_id):
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

        text = f'{user_full_name}, оставил запись: {message}'

        if send_to_telegram(text) != 200:
            Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListView(generics.ListAPIView):
    queryset = MessageOnWall.objects.all()
    serializer_class = MessageOnWallSerializer
