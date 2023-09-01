from .models import *
from rest_framework.serializers import ModelSerializer, ValidationError, ReadOnlyField
from django.db.models import Avg
from review.serializers import CommentSerializer
from review.models import Comment

# class ValidationMixin():
#      def validate_title(self, title):
#         if self.Meta.model.objects.filter(title=title).exists():
#             raise ValidationError(
#                 'Такое название уже существует'
#             )
#         return title

class CategorySerializer(ModelSerializer):
     
    class Meta:
        model = Category
        fields = ('title',)


class TagSerializer(ModelSerializer):
    class Meta:
        model = Tag
        fields = ('title',)


class PostDetailSerializer(ModelSerializer):
    author = ReadOnlyField(source='author.name')

    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags', [])
        post = Post.objects.create(author=user, **validated_data)
        post.tags.add(*tags)
        return post
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['rating'] = instance.ratings.aggregate(Avg('rating'))['rating__avg']
        representation['comments'] = CommentSerializer(Comment.objects.filter(post=instance.pk), many=True).data
        return representation

    class Meta:
        model = Post
        fields = '__all__'



class PostListSerializer(ModelSerializer):
   
    class Meta:
        model = Post
        fields = ['author','title', 'body']     
        
    