from django.shortcuts import render


from .models import File, Work
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import FileSerializer, WorkSerializer


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all().order_by('-created_at')
    serializer_class = FileSerializer
    # permission_classes = [permissions.IsAuthenticated]


class WorkViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows musical works to be viewed or edited.
    """
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    # permission_classes = [permissions.IsAuthenticated]