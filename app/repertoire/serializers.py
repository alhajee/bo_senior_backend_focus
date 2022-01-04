from .models import File, Contributor, Work
from rest_framework import serializers


class FileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = File
        fields = ['filename', 'work_count', 'created_at']


class WorkSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Work
        fields = ['iswc', 'title', 'contributors', 'source', 'proprietary_id']