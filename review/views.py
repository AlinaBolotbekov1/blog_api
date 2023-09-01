from rest_framework.viewsets import ModelViewSet
from .models import Comment, Rating, Like
from .serializers import CommentSerializer
from post.permissions import IsAdminPermission, IsAuthorPermission
from rest_framework.permissions import AllowAny
from rest_framework import generics

class PermissionMixin:
    def get_permissions(self):
        
        if self.action == 'create':
            self.permission_classes = [IsAdminPermission]

        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthorPermission]
        
        elif self.action in ['list', 'retrieve']:
            self.permission_classes = [AllowAny]
        return super().get_permissions()



class CommentView(PermissionMixin,ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer



# class RatingView(PermissionMixin,ModelViewSet):
#     queryset = Rating.objects.all()
#     serializer_class = RatingSerializer

#     def  check_action(self):
#         if self.action == 'create':


# stack overflow

 
       