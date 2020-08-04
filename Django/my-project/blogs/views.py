from django.http import JsonResponse
from .models import Blog
from .serializers import BlogSerializer
from rest_framework import generics


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


class BlogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()