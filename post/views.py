from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from review.models import Rating
from rest_framework.response import Response
from .serializers import *
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, filters
import django_filters
from rest_framework.permissions import AllowAny
from .permissions import IsAuthorPermission, IsAdminPermission
from rest_framework.decorators import action
from review.serializers import RatingSerializer
from review.models import Like

User = get_user_model()



# class CategoryView(APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data, status=200)
    

# class PostView(APIView):
#     def get(self, requests):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many=True)
#         return Response(serializer.data, status=200)
    

#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response('Пост успешно создан', status=201)
        

#     def delete(self, request, pk):
#         post = get_object_or_404(Post, pk=pk)
#         post.delete()
#         return Response('Пост успешно удален', status=204)

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

                     

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return PostListSerializer
        return PostDetailSerializer


class PostRetriveView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags__slug', 'category', 'author']
    search_fields = ['title', 'body'] 
    ordering_fields = ['created_at', 'title'] 

    @action(methods=['POST', 'PATCH'], detail=True)
    def set_rating(self, request, pk=None):
        # data = request.data
        data = request.data.copy()
        data['post'] = pk
        serializer = RatingSerializer(
            data=data, 
            context = {'request': request}
            )
        rating = Rating.objects.filter(
            author=request.user, 
            post=pk
            ).first()
        if serializer.is_valid(raise_exception=True):
            if rating and request.method == 'POST':
                return Response(
                    'Rating object exists',
                    status=200
                )
            elif rating and request.method == 'PATCH':
                serializer.update(rating, serializer.validated_data)

                return Response(
                    serializer.data, status=200
                )
            elif request.method == 'POST':
                serializer.create(serializer.validated_data)
                return Response(
                    serializer.data,
                    status=201
                )


    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        try:
            like = Like.objects.get(post=post, author=user)
            print('=======================================')
            print(like)
            print('=======================================')
            like.delete()
            message = 'Disliked'
            status = 204

        except Like.DoesNotExist:
            Like.objects.create(post=post, author=user)
            message == 'Liked'
            status = 201
        return Response(message, status=status)






    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostDetailSerializer
    

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAdminPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()