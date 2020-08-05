from django.http import JsonResponse
from .models import Blog
from .serializers import BlogSerializer
from .permissions import IsAuthor, ReadOnly
from rest_framework import generics

from rest_framework.permissions import IsAuthenticatedOrReadOnly
# from rest_framework.permissions.decurators import permission_class


# Create your views here.

def hello(request):
    #processing
    dic = {
        'name': 'RAM',
        'address': "kathmandu"
    }
    return JsonResponse(dic)


class BlogListCreate(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes  = [IsAuthenticatedOrReadOnly]


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    permission_classes = [IsAuthor | ReadOnly]