from rest_framework import serializers
from .models import Blog, Comment
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Comment
        fields = '__all__'

class BlogListSerializer(serializers.ModelSerializer):

    author = UserSerializer(required=False)
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ["author"]

    def create(self, validated_data, *args, **kwargs):
        validated_data["author"] = self.context["request"].user
        return super().create(validated_data, *args, **kwargs)


class BlogDetailSerializer(serializers.ModelSerializer):

    comments = serializers.SerializerMethodField()
    author = UserSerializer()
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields  = ["author", "comments"]
    
    def get_comments(self, obj):
        commnets_qs = Comment.objects.filter(blog=obj) 
        serialized_data = CommentDetailSerializer(commnets_qs, many=True).data
        return serialized_data



