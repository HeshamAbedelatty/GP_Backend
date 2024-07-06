# serializers.py
from rest_framework import serializers

class RecommendationSerializer(serializers.Serializer):
    username = serializers.CharField()
    recommended_groups = serializers.ListField(child=serializers.CharField())