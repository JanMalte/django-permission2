# coding=utf-8
from django.test import TestCase, override_settings

from ... import add_permission_logic
from ...logics import AuthorPermissionLogic
from ..compat import MagicMock
from ..utils import create_anonymous, create_article, create_user


@override_settings(
    PERMISSION_DEFAULT_APL_FIELD_NAME="author",
    PERMISSION_DEFAULT_APL_ANY_PERMISSION=True,
    PERMISSION_DEFAULT_APL_CHANGE_PERMISSION=True,
    PERMISSION_DEFAULT_APL_DELETE_PERMISSION=True,
)
class PermissionLogicsAuthorPermissionLogicTestCase(TestCase):
    def setUp(self):
        self.user1 = create_user("john")
        self.user2 = create_user("tony")
        self.anonymous = create_anonymous()
        self.perm1 = "permission.add_article"
        self.perm2 = "permission.change_article"
        self.perm3 = "permission.delete_article"
        self.article = create_article("test", user=self.user2)

    def test_constructor(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, AuthorPermissionLogic))
        self.assertEqual(permission_logic.field_name, "author")
        self.assertEqual(permission_logic.any_permission, True)
        self.assertEqual(permission_logic.change_permission, True)
        self.assertEqual(permission_logic.delete_permission, True)

    def test_constructor_with_specifing_field_name(self):
        permission_logic = AuthorPermissionLogic(field_name="specified")
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, AuthorPermissionLogic))
        self.assertEqual(permission_logic.field_name, "specified")

    def test_constructor_with_specifing_any_permission(self):
        permission_logic = AuthorPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, AuthorPermissionLogic))
        self.assertEqual(permission_logic.any_permission, False)

    def test_constructor_with_specifing_change_permission(self):
        permission_logic = AuthorPermissionLogic(change_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, AuthorPermissionLogic))
        self.assertEqual(permission_logic.change_permission, False)

    def test_constructor_with_specifing_delete_permission(self):
        permission_logic = AuthorPermissionLogic(delete_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(isinstance(permission_logic, AuthorPermissionLogic))
        self.assertEqual(permission_logic.delete_permission, False)

    def test_has_perm_add_without_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm1))

    def test_has_perm_change_without_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm2))

    def test_has_perm_delete_without_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user1, self.perm3))

    def test_has_perm_add_without_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm1))

    def test_has_perm_change_without_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm2))

    def test_has_perm_delete_without_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(permission_logic.has_perm(self.anonymous, self.perm3))

    def test_has_perm_add_with_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user1, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user1, self.perm2, self.article)
        )

    def test_has_perm_delete_with_obj(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user1, self.perm3, self.article)
        )

    def test_has_perm_add_with_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm2, self.article)
        )

    def test_has_perm_delete_with_obj_with_anonymous(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.anonymous, self.perm3, self.article)
        )

    def test_has_perm_add_with_obj_author(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm1, self.article))

    def test_has_perm_change_with_obj_author(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm2, self.article))

    def test_has_perm_delete_with_obj_author(self):
        permission_logic = AuthorPermissionLogic()
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm3, self.article))

    def test_has_perm_add_with_obj_author_diff_field_name(self):
        permission_logic = AuthorPermissionLogic(field_name="editor")
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj_author_diff_field_name(self):
        permission_logic = AuthorPermissionLogic(field_name="editor")
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm2, self.article)
        )

    def test_has_perm_delete_with_obj_author_diff_field_name(self):
        permission_logic = AuthorPermissionLogic(field_name="editor")
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm3, self.article)
        )

    def test_has_perm_add_with_obj_author_non_any(self):
        permission_logic = AuthorPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj_author_non_any(self):
        permission_logic = AuthorPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm2, self.article))

    def test_has_perm_delete_with_obj_non_any(self):
        permission_logic = AuthorPermissionLogic(any_permission=False)
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm3, self.article))

    def test_has_perm_add_with_obj_author_non_any_no_change(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, change_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj_author_non_any_no_change(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, change_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm2, self.article)
        )

    def test_has_perm_delete_with_obj_non_any_no_change(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, change_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm3, self.article))

    def test_has_perm_add_with_obj_author_non_any_no_delete(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, delete_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm1, self.article)
        )

    def test_has_perm_change_with_obj_author_non_any_no_delete(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, delete_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertTrue(permission_logic.has_perm(self.user2, self.perm2, self.article))

    def test_has_perm_delete_with_obj_non_any_no_delete(self):
        permission_logic = AuthorPermissionLogic(
            any_permission=False, delete_permission=False
        )
        add_permission_logic(self.article.__class__, permission_logic)
        self.assertFalse(
            permission_logic.has_perm(self.user2, self.perm3, self.article)
        )
