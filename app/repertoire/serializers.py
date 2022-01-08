from .models import File, Contributor, Work
from rest_framework import serializers
from rest_framework.reverse import reverse


class WorkSerializer(serializers.ModelSerializer):
    contributors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
    class Meta:
        model = Work    
        fields = ['id', 'proprietary_id', 'iswc', 'source', 'title', 'contributors']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'filename', 'work_count']


class FileWorksSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    works = WorkSerializer(many=True)
    file = FileSerializer(many=True)