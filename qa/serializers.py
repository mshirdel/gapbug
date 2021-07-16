from rest_framework import serializers
from .models import Comment, CommentVote
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


# Comment Serializers

class CommentListRetrieveSerializer(serializers.ModelSerializer):
    """ Comment Serializer for list, retrieve actions """
    
    # model__in=["question", "answer"] because we only leave comments under Questions or Answers
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(model__in=["question", "answer"]),
        slug_field='model',
    )
    # Add additional read-only fields to serialzier like this
    user__username = serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model = Comment
        fields = "__all__"

class CommentCreateSerializer(serializers.ModelSerializer):
    """ Comment Serializer for create action """
    
    # model__in=["question", "answer"] because we only leave comments under Questions or Answers
    content_type = serializers.SlugRelatedField(
        queryset=ContentType.objects.filter(model__in=["question", "answer"]),
        slug_field='model',
    )
    
    def validate(self, attrs):
        vd = super().validate(attrs)
        
        content_type = vd.get("content_type")
        # For more information about DynamicModel check the link below:
        # https://stackoverflow.com/questions/68093630/how-to-query-multiple-models-in-django-using-a-variable-as-the-models-name/68093727#68093727
        DynamicModel = apps.get_model(content_type.app_label, content_type.model)
        
        try:
            obj = DynamicModel.objects.get(id=vd.get("object_id"))
        except DynamicModel.DoesNotExist:
            # Couldn't find an object based on content_type and object_id
            raise serializers.ValidationError("سوال و یا جوابی برای ثبت نظر پیدا نشد.")
        
        return vd
    
    class Meta:
        model = Comment
        exclude = ["user", "vote",]

class CommentPartialUpdateSerializer(serializers.ModelSerializer):
    """  
    Comment Serializer for partial_update action 
        Note:
            We don't update a comment but it's text, so it's partial_update not update.
    """
    
    class Meta:
        model = Comment
        fields = ["text"]
        