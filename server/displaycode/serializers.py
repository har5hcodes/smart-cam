from django.contrib.auth.models import User, Group
from rest_framework import serializers
from displaycode.models import Snippet, Comment, WaitListUser, Camera, SnapshotDetails
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        #fields = ['username', 'email']
        #fields = '__all__'
        fields = ['id', 'url', 'username', 'email', 'groups', 'snippets']

class CommentSerializer(serializers.HyperlinkedModelSerializer):

    #https://wsvincent.com/django-rest-framework-changing-field-names/
    line = serializers.IntegerField()

    class Meta:
        model = Comment
        #fields = ['author', 'code']
        fields = ['id', 'author', 'snippetId', 'text', 'line', 'published_date']

class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    #comment = CommentSerializer()
    comments = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Snippet
        fields = ['id', 'author', 'text', 'language', 'title', 'comments']
        #depth = 1
        #fields = ['code']

    def get_comments(self, snippet):
        commentObjects = Comment.objects.filter(snippetId=snippet.id)
        commentIds = []
        for obj in commentObjects:
            commentIds.append(obj.id)

        return commentIds

class WaitListUserSerializer(serializers.HyperlinkedModelSerializer):

    #https://wsvincent.com/django-rest-framework-changing-field-names/
    #line = serializers.IntegerField()

    class Meta:
        model = WaitListUser
        fields = ['id', 'email', 'username', 'aboutme', 'painpoints', 'joinedDate', 'referralUrl']

#https://joel-hanson.medium.com/drf-how-to-make-a-simple-file-upload-api-using-viewsets-1b1e65ed65ca
#from rest_framework import serializers.Serializer
from rest_framework.serializers import FileField

# Serializers define the API representation.
class UploadSerializer(serializers.Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']


#class GroupSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Group
#        fields = ['url', 'name']



class CameraSerializer(serializers.HyperlinkedModelSerializer): 

    class Meta:
        model = Camera
        fields = ['camId', 'camUrl', 'camLoc', 'metadata']



class SnapshotDetailsSerializer(serializers.HyperlinkedModelSerializer): 

    class Meta:
        model = SnapshotDetails
        fields = ['snapshotId', 'dirLoc', 'capturedTime', 'camera']