from .models import File, Contributor, Work
from rest_framework import serializers
from rest_framework.reverse import reverse


class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contributor
        fields = ['name']


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['id', 'proprietary_id', 'iswc', 'source', 'title', 'contributors']


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'filename', 'work_count']


class WorksSerializer(serializers.Serializer):
    class Meta:
        works = WorkSerializer(many=True)
        files = FileSerializer(many=True)
        count = 1
        fields = ['count', 'files', 'works']


