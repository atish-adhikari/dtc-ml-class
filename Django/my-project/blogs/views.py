from django.http import JsonResponse
from .models import Blog, Comment
from .serializers import BlogSerializer, BlogListSerializer, BlogDetailSerializer, CommentSerializer
from .permissions import IsAuthor, ReadOnly
from rest_framework import generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

def hello(request):
    #processing
    dic = {
        'name': 'RAM',
        'address': "kathmandu"
    }
    return JsonResponse(dic)


class BlogListCreate(generics.ListCreateAPIView):
    permission_classes  = [IsAuthenticatedOrReadOnly]
    queryset = Blog.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return BlogListSerializer
        return BlogSerializer

    def post(self, request, *args, **kwargs):
        request.data["author"] = request.user.id
        return super(BlogListCreate, self).post(request, *args, **kwargs)


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAuthor | ReadOnly]
    
    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return BlogDetailSerializer
        return BlogSerializer


class CommentListCreate(generics.ListCreateAPIView):
    permission_classes  = [IsAuthenticatedOrReadOnly]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthor | ReadOnly]