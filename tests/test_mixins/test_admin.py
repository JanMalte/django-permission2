from unittest.mock import patch

from django.contrib import admin
from django.test import RequestFactory, TestCase

from permission.mixins.admin import RequireObjectPermissionAdminMixin
from tests.compat import MagicMock
from tests.models import Article
from tests.utils import create_article, create_user


class ArticleAdmin(RequireObjectPermissionAdminMixin, admin.ModelAdmin):
    pass


# @override_settings(
#     AUTHENTICATION_BACKENDS=(
#         "django.contrib.auth.backends.ModelBackend",
#         "permission.backends.PermissionBackend",
#     ),
# )
class RequireObjectPermissionAdminMixinTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_user("john")
        self.article = create_article("test", user=self.user)
        self.model_admin = ArticleAdmin(Article, admin.site)

    def _get_request(self, user=None):
        request = self.factory.get("/")
        request.user = user or self.user
        return request

    def test_build_perm_string(self):
        self.assertEqual(
            self.model_admin._build_perm_string("view"),
            "permission.view_article",
        )
        self.assertEqual(
            self.model_admin._build_perm_string("change"),
            "permission.change_article",
        )
        self.assertEqual(
            self.model_admin._build_perm_string("delete"),
            "permission.delete_article",
        )

    def test_has_view_permission_without_obj_delegates_to_super(self):
        """Without obj the mixin should fall through to ModelAdmin default."""
        request = self._get_request()
        sentinel = object()
        with patch.object(admin.ModelAdmin, "has_view_permission", return_value=sentinel) as mock_super:
            result = self.model_admin.has_view_permission(request, obj=None)
        mock_super.assert_called_once_with(request, None)
        self.assertIs(result, sentinel)

    def test_has_view_permission_with_obj_granted(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=True)
        self.assertTrue(self.model_admin.has_view_permission(request, obj=self.article))
        request.user.has_perm.assert_called_with("permission.view_article", self.article)

    def test_has_view_permission_with_obj_denied(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=False)
        self.assertFalse(self.model_admin.has_view_permission(request, obj=self.article))

    def test_has_view_permission_with_obj_falls_back_to_change(self):
        """View perm denied but change perm granted → should return True."""
        request = self._get_request()
        request.user.has_perm = MagicMock(side_effect=lambda perm, obj=None: perm == "permission.change_article")
        self.assertTrue(self.model_admin.has_view_permission(request, obj=self.article))

    def test_has_change_permission_without_obj_delegates_to_super(self):
        request = self._get_request()
        sentinel = object()
        with patch.object(admin.ModelAdmin, "has_change_permission", return_value=sentinel) as mock_super:
            result = self.model_admin.has_change_permission(request, obj=None)
        mock_super.assert_called_once_with(request, None)
        self.assertIs(result, sentinel)

    def test_has_change_permission_with_obj_granted(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=True)
        self.assertTrue(self.model_admin.has_change_permission(request, obj=self.article))
        request.user.has_perm.assert_called_with("permission.change_article", self.article)

    def test_has_change_permission_with_obj_denied(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=False)
        self.assertFalse(self.model_admin.has_change_permission(request, obj=self.article))

    def test_has_delete_permission_without_obj_delegates_to_super(self):
        request = self._get_request()
        sentinel = object()
        with patch.object(admin.ModelAdmin, "has_delete_permission", return_value=sentinel) as mock_super:
            result = self.model_admin.has_delete_permission(request, obj=None)
        mock_super.assert_called_once_with(request, None)
        self.assertIs(result, sentinel)

    def test_has_delete_permission_with_obj_granted(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=True)
        self.assertTrue(self.model_admin.has_delete_permission(request, obj=self.article))
        request.user.has_perm.assert_called_with("permission.delete_article", self.article)

    def test_has_delete_permission_with_obj_denied(self):
        request = self._get_request()
        request.user.has_perm = MagicMock(return_value=False)
        self.assertFalse(self.model_admin.has_delete_permission(request, obj=self.article))

    def test_has_add_permission_is_not_overridden(self):
        self.assertNotIn("has_add_permission", RequireObjectPermissionAdminMixin.__dict__)

    def test_has_module_permission_is_not_overridden(self):
        self.assertNotIn("has_module_permission", RequireObjectPermissionAdminMixin.__dict__)
