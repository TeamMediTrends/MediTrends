from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin to restrict access to admin users only."""

    def test_func(self):
        """Only allow superusers to access the view."""
        return self.request.user.is_superuser  # Use is_staff instead if needed

    def handle_no_permission(self):
        """Redirect or show an error when access is denied."""
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied  # You can change this to redirect if preferred
