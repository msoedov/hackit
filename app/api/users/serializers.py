from rest_framework import serializers

from .models import User, File


class UserWithDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class FileSerializer(serializers.ModelSerializer):
    download_link = serializers.HyperlinkedIdentityField('download',
                                                         lookup_field='name')

    class Meta:
        model = File
        fields = '__all__'
