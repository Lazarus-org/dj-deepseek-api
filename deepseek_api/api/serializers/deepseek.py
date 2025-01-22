# chat/serializers.py
from rest_framework import serializers

class DeepSeekChatSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=1000)
    model = serializers.CharField(max_length=100, required=False, default="deepseek-chat")
    temperature = serializers.FloatField(required=False, default=0.7)
    max_tokens = serializers.IntegerField(required=False, default=1000)