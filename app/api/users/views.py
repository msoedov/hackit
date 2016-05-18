import os
from django.conf import settings
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from .models import File
from .serializers import FileSerializer


class AuthRequired(object):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)


class FilesListView(AuthRequired, ListAPIView):
    """
    A view that permits a GET to allow listing all the Files
    in the database

    Route - `/reviews`
    """
    serializer_class = FileSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return File.objects.filter(owner=self.request.user)


class FileView(AuthRequired, RetrieveUpdateAPIView):
    """
    A view that permits a GET to allow listing of a single File
    by providing their `id` as a parameter

    Route - `/reviews/:name`
    """
    serializer_class = FileSerializer
    pagination_class = None
    lookup_field = 'name'

    def get_queryset(self):
        return File.objects.get(owner=self.request.user,
                                name=self.kwargs.get('name', ''))

    def put(self, request, *args, **kwargs):
        name = kwargs.get('name')
        file_path = "{}/{}".format(settings.FILES_VOLUME, name)
        dirname = os.path.dirname(os.path.realpath(file_path))
        os.makedirs(dirname, exist_ok=True)
        with open(file_path, 'wb') as fp:
            fp.write(request.body)
        file, created = File.objects.get_or_create(owner=request.user,
                                                   name=name)
        if not created:
            file.revision += 1
            file.save()
        return Response(data={})


class DownloadView(AuthRequired, RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        get_object_or_404(File, owner=self.request.user, name=name)
        file_path = "{}/{}".format(settings.FILES_VOLUME, name)
        with open(file_path, 'rb') as fp:
            data = fp.read()
        return HttpResponse(content=data,
                            content_type='application/octet-stream')
