from rest_framework import serializers
from .models import FQA, QuestionLog, HandoffRequest


class ChatRequestSerializer(serializers.ModelSerializer):
    message = serializers.CharField()
    lang = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = QuestionLog
        fields = ("message", "lang")

class chatResponseSerializer(serializers.Serializer):
    reply = serializers.CharField()
    lang = serializers.CharField()
    matched_fqa_id = serializers.IntegerField(allow_null=True)
    confidence = serializers.FloatField()

class HandoffRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HandoffRequest
        fields = ("name", "contact", "message")
