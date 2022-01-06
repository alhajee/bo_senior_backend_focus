from collections import namedtuple

# import get_object_or_404()
from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response

from .models import Contributor, File, Work
from .serializers import FileSerializer, WorksSerializer


Files = namedtuple('Files', ('files', 'works', 'count'))


class FileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows files to be viewed or edited.
    """
    queryset = File.objects.all().order_by('-created_at')
    serializer_class = FileSerializer
    # permission_classes = [permissions.IsAuthenticated]


# class WorkViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows musical works to be viewed or edited.
#     """
#     queryset = Work.objects.all()
#     serializer_class = WorkSerializer
#     # permission_classes = [permissions.IsAuthenticated]


# class FilesViewSet(viewsets.ViewSet):
#     """
#     A simple ViewSet for listing files and works
#     """
#     def list(self, request):
#         files = Files(
#             files=File.objects.all(),
#             works=Work.objects.all(),
#         )
#         serializer = FilesSerializer(files)
#         return Response(serializer.data)


class WorksViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    # def get_queryset(self):
    #     """
    #     This view should return a list of all the purchases for
    #     the user as determined by the username portion of the URL.
    #     """
    #     username = self.kwargs['username']
    #     return Purchase.objects.filter(purchaser__username=username)

    def list(self, request, file_id):
    
        # self.kwargs['username']

        file_queryset = File.objects.all()
        file = get_object_or_404(file_queryset, pk=file_id)

        queryset = Work.objects.filter(file=file)
        
        serializer = WorksSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, file_id, pk=None):
        queryset = File.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = FileSerializer(user)
        return Response(serializer.data)
    