from collections import namedtuple

# import get_object_or_404()
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .models import (
    File, 
    Work
)
from .serializers import (
    FileSerializer, 
    WorkSerializer, 
    FileWorksSerializer
)


class FileViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for listing or retrieving files and works
    """
    queryset = File.objects.all().order_by('-created_at')
    serializer_class = FileSerializer


class WorksViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving files and works
    """

    # tuple to send data across to a serializer
    FileWorks = namedtuple(
        'FileWorks', 
        ('file', 'works', 'count')
    )


    def list(self, request, file_id):
        """
        handles /files/<file_id>/works/
        """
        # get the file
        file_queryset = File.objects.all()
        file = get_object_or_404(file_queryset, pk=file_id)
        # get all works in that file
        works_queryset = Work.objects.filter(file=file)
        # get length of query result
        count = works_queryset.__len__
        # pass in the required data to the serializer
        fileworks = self.FileWorks(
            count=count,
            file=file_queryset,
            works=works_queryset,
        )
        serializer = FileWorksSerializer(fileworks)
        return Response(serializer.data)


    def retrieve(self, request, file_id, pk):
        """
        handles /files/<file_id>/works/<work_id>
        """
        # query all files
        file_queryset = File.objects.all()
        # get file with the file_id
        file = get_object_or_404(file_queryset, pk=file_id)
        # query all works
        work_queryset = Work.objects.all()
        # get work with the given work_id
        work = get_object_or_404(work_queryset, pk=pk)
        # send query to serializer
        serializer = WorkSerializer(work)
        return Response(serializer.data)
    