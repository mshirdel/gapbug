from django.contrib.auth.mixins import PermissionRequiredMixin
from .privilages import Privilages


class PrivilageRequiredMixin(PermissionRequiredMixin):
    privilage_required = None

    def has_permission(self) -> bool:
        if self.privilage_required:
            return Privilages(self.request.user).check_privilage(
                self.privilage_required
            )
        return False
