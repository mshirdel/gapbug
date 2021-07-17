from django.shortcuts import get_object_or_404
from qa.models import Comment
from django.contrib.auth.mixins import PermissionRequiredMixin
from .privilages import Privilages
from django.core.exceptions import PermissionDenied


class PrivilageRequiredMixin(PermissionRequiredMixin):
    """
    Check required privilages in views.
    """

    privilage_required = None

    def has_permission(self) -> bool:
        if self.privilage_required:
            return Privilages(self.request.user).check_privilage(
                self.privilage_required
            )
        return False


class OnlyCommentOwnerMixin:
    
    #TODO Who can edit comments ? couldn't find any privilage.
    def dispatch(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(Comment, pk=pk)
        if request.user != obj.user:
            raise PermissionDenied
        return super().dispatch(request, pk, *args, **kwargs)
    