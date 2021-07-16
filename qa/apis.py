
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models import Comment
from .serializers import (
    CommentListRetrieveSerializer, CommentCreateSerializer, CommentPartialUpdateSerializer,
)


class CommentViewSet(ModelViewSet):
    
    queryset = Comment.objects.select_related("user").all()
    http_method_names = ["get", "post", "patch", "delete"]
    filter_backends = [DjangoFilterBackend,]
    
    # content_type__model is the model name in this case it can be 'question' or 'answer'
    # because we can only leave commnets under Questions or Answers
    # .../?content_type__model=question&object_id=question_id will give us comments of a Question
    # .../?content_type__model=answer&object_id=answer_id will give us comments of a Answer
    filterset_fields = ["id", "content_type__model", "object_id",]
    
    def get_serializer_class(self):
        
        if self.action == "create":
            return CommentCreateSerializer
        elif self.action == "partial_update":
            return CommentPartialUpdateSerializer
        
        # action == "list" or action == "retrieve"
        return CommentListRetrieveSerializer
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    

#TODO Add CommentVoteViewSet
