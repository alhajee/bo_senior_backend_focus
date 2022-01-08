from .models import File, Contributor, Work
from rest_framework import serializers
from rest_framework.reverse import reverse


class WorkSerializer(serializers.ModelSerializer):
    contributors = serializers.StringRelatedField(
        many=True,
        read_only=True,
    )
    class Meta:
        model = Work    
        fields = ['id', 'proprietary_id', 'iswc', 'source', 'title', 'contributors']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'filename', 'work_count']


class WorksSerializer(serializers.Serializer):
    works = WorkSerializer(many=True)
    files = FileSerializer(many=True)
    count = 1
    class Meta:
        fields = ['count', 'files', 'works']


