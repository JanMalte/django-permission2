Admin Integration
=================

Object-level permissions in Django Admin
----------------------------------------

By default, Django's ``ModelAdmin`` only checks model-level permissions
(e.g. *"can this user change any article?"*).  It does **not** pass the
object to ``has_perm``, so object-level permission logics registered with
django-permission2 are never consulted in the admin.

``RequireObjectPermissionAdminMixin`` fixes this.  When mixed into a
``ModelAdmin``, it overrides ``has_view_permission``,
``has_change_permission``, and ``has_delete_permission`` so that whenever
an object is available, the check is delegated to
``request.user.has_perm(perm, obj)`` — which triggers django-permission2's
registered permission logics.

When no object is available (e.g. on list views), the mixin falls through
to Django's default model-level permission check.

``has_add_permission`` and ``has_module_permission`` are **not** overridden
because they do not operate on a specific object.

Usage
~~~~~

.. code:: python

    from django.contrib import admin
    from permission.mixins.admin import RequireObjectPermissionAdminMixin

    from myapp.models import Article


    class ArticleAdmin(RequireObjectPermissionAdminMixin, admin.ModelAdmin):
        pass


    admin.site.register(Article, ArticleAdmin)

.. note::

    Place the mixin **before** ``admin.ModelAdmin`` in the class bases so
    that its methods take precedence.
