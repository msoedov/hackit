from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^reviews$',
        FilesListView.as_view(),
        name='file-list'),
    url(r'^reviews/(?P<name>\w+?\.\w+)$',
        FileView.as_view(),
        name='file-detail'),
    url(r'^reviews/download/(?P<name>\w+?\.\w+)$',
        DownloadView.as_view(),
        name='download'),
]
