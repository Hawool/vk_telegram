from rest_framework.serializers import ModelSerializer

from vk_telegram.models import MessageOnWall


class MessageOnWallSerializer(ModelSerializer):
    class Meta:
        model = MessageOnWall
        fields = '__all__'
