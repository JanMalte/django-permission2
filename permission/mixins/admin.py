"""
Admin mixin for object-level permission checks via django-permission2.

When mixed into a ``ModelAdmin``, the mixin overrides
``has_view_permission``, ``has_change_permission``, and
``has_delete_permission`` so that object-level permissions are checked
through Django's ``has_perm`` (and therefore through any registered
``PermissionBackend`` and permission logics) whenever an *obj* is provided.

When *obj* is ``None`` (e.g. on list views), the mixin defers to the
default ``ModelAdmin`` behaviour.
"""

__all__ = ("RequireObjectPermissionAdminMixin",)


class RequireObjectPermissionAdminMixin:
    """
    ModelAdmin mixin that delegates object-level permission checks to
    ``request.user.has_perm(perm, obj)``.

    Only ``has_view_permission``, ``has_change_permission``, and
    ``has_delete_permission`` are overridden.  ``has_add_permission`` and
    ``has_module_permission`` are left untouched.

    Usage::

        from django.contrib import admin
        from permission.mixins.admin import RequireObjectPermissionAdminMixin

        class ArticleAdmin(RequireObjectPermissionAdminMixin, admin.ModelAdmin):
            pass
    """

    def _build_perm_string(self, action):
        """Return ``'app_label.action_modelname'`` for the administered model."""
        opts = self.model._meta
        return f"{opts.app_label}.{action}_{opts.model_name}"

    def has_view_permission(self, request, obj=None):
        if obj is None:
            return super().has_view_permission(request, obj)
        perm_view = self._build_perm_string("view")
        perm_change = self._build_perm_string("change")
        return request.user.has_perm(perm_view, obj) or request.user.has_perm(perm_change, obj)

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return super().has_change_permission(request, obj)
        return request.user.has_perm(self._build_perm_string("change"), obj)

    def has_delete_permission(self, request, obj=None):
        if obj is None:
            return super().has_delete_permission(request, obj)
        return request.user.has_perm(self._build_perm_string("delete"), obj)
