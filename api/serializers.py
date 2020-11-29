from rest_framework import serializers
class TeamSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    score = serializers.IntegerField()
    link = serializers.CharField()
    url = serializers.CharField()