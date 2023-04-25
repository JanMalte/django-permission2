Permissions
============

Apply permission logic
----------------------
Let's assume you wrote an article model which has an ``author`` attribute to store the creator of the article, and you want to give that author full control permissions
(e.g. add, change and delete permissions).

What you need to do is just applying ``permission.logics.AuthorPermissionLogic``
to the ``Article`` model like

.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic())


.. note::
    You can specify related object with `field__name` attribute like
    `django queryset lookup <https://docs.djangoproject.com/en/1.10/topics/db/queries/#field-lookups>`_.
    See the working example below:

.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        project = models.ForeignKey('permission.Project')

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    class Project(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic to Article
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic(
        field_name='project__author',
    ))


That's it.
Now the following codes will work as expected:


.. code:: python

    user1 = User.objects.create_user(
        username='john',
        email='john@test.com',
        password='password',
    )
    user2 = User.objects.create_user(
        username='alice',
        email='alice@test.com',
        password='password',
    )

    art1 = Article.objects.create(
        title="Article 1",
        body="foobar hogehoge",
        author=user1
    )
    art2 = Article.objects.create(
        title="Article 2",
        body="foobar hogehoge",
        author=user2
    )

    # Grant the `permission.add_article` permission for user1.
    # Use the `perm_to_permission` utility to convert the permission-string to a `Permission` object instance.
    from permission.utils.permissions import perm_to_permission
    user1.user_permissions.add(perm_to_permission('permission.add_article'))

    # `add_article` is granted by user permissions
    assert user1.has_perm('permission.add_article') == True
    assert user2.has_perm('permission.add_article') == False

    # `change_article` is not granted by user permissions
    assert user1.has_perm('permission.change_article') == False
    assert user2.has_perm('permission.change_article') == False

    # `change_article` is granted by `AuthorPermissionLogic`
    assert user1.has_perm('permission.change_article', art1) == True
    # `change_article` is not granted by `AuthorPermissionLogic`
    assert user1.has_perm('permission.change_article', art2) == False

    # `delete_article` is not granted by user permissions
    assert user1.has_perm('permission.delete_article') == False
    assert user2.has_perm('permission.delete_article') == False

    # `delete_article` is granted by `AuthorPermissionLogic`
    assert user1.has_perm('permission.delete_article', art1) == True
    # `delete_article` is not granted by `AuthorPermissionLogic`
    assert user1.has_perm('permission.delete_article', art2) == False

    # `delete_article` is not granted by `AuthorPermissionLogic`
    assert user2.has_perm('permission.delete_article', art1) == False
    # `delete_article` is granted by `AuthorPermissionLogic`
    assert user2.has_perm('permission.delete_article', art2) == True

    #
    # You may also be interested in django signals to apply 'add' permissions to the
    # newly created users.
    # https://docs.djangoproject.com/en/dev/ref/signals/#django.db.models.signals.post_save
    #
    from django.db.models.signals.post_save
    from django.dispatch import receiver
    from permission.utils.permissions import perm_to_permission

    @receiver(post_save, sender=User)
    def apply_permissions_to_new_user(sender, instance, created, **kwargs):
        if not created:
            return
        #
        # permissions you want to apply to the newly created user
        # YOU SHOULD NOT APPLY PERMISSIONS EXCEPT PERMISSIONS FOR 'ADD'
        # in this way, the applied permissions are not object permission so
        # if you apply 'permission.change_article' then the user can change
        # any article object.
        #
        permissions = [
            'permission.add_article',
        ]
        for permission in permissions:
            # apply permission
            # perm_to_permission is a utility to convert string permission
            # to permission instance.
            instance.user_permissions.add(perm_to_permission(permission))


See :class:`permission.logics.author.AuthorPermissionLogic` to learn how this logic works.

Now, assume you add ``collaborators`` attribute to store collaborators
of the article and you want to give them a change permission.

What you need to do is quite simple.
Apply ``permission.logics.CollaboratorsPermissionLogic``
to the ``Article`` model as follows


.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        author = models.ForeignKey(User)
        collaborators = models.ManyToManyField(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic and CollaboratorsPermissionLogic
    from permission import add_permission_logic
    from permission.logics import AuthorPermissionLogic
    from permission.logics import CollaboratorsPermissionLogic
    add_permission_logic(Article, AuthorPermissionLogic())
    add_permission_logic(Article, CollaboratorsPermissionLogic(
        field_name='collaborators',
        any_permission=False,
        change_permission=True,
        delete_permission=False,
    ))


.. note::
    You can specify related object with `field_name` attribute like
    `django queryset lookup <https://docs.djangoproject.com/en/1.10/topics/db/queries/#field-lookups>`_.
    See the working example below:


.. code:: python

    from django.db import models
    from django.contrib.auth.models import User


    class Article(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        project = models.ForeignKey('permission.Project')

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    class Project(models.Model):
        title = models.CharField('title', max_length=120)
        body = models.TextField('body')
        collaborators = models.ManyToManyField(User)

        # this is just required for easy explanation
        class Meta:
            app_label='permission'

    # apply AuthorPermissionLogic to Article
    from permission import add_permission_logic
    from permission.logics import CollaboratorsPermissionLogic
    add_permission_logic(Article, CollaboratorsPermissionLogic(
        field_name='project__collaborators',
    ))


That's it.
Now the following codes will work as expected:


.. code:: python

    user1 = User.objects.create_user(
        username='john',
        email='john@test.com',
        password='password',
    )
    user2 = User.objects.create_user(
        username='alice',
        email='alice@test.com',
        password='password',
    )

    art1 = Article.objects.create(
        title="Article 1",
        body="foobar hogehoge",
        author=user1
    )
    art1.collaborators.add(user2)

    assert user1.has_perm('permission.change_article') == False
    assert user1.has_perm('permission.change_article', art1) == True
    assert user1.has_perm('permission.delete_article', art1) == True

    assert user2.has_perm('permission.change_article') == False
    assert user2.has_perm('permission.change_article', art1) == True
    assert user2.has_perm('permission.delete_article', art1) == False


See :class:`permission.logics.collaborators.CollaboratorsPermissionLogic` to learn how this logic works.

There are :class:`permission.logics.staff.StaffPermissionLogic` and
:class:`permission.logics.groupinGroupInPermissionLogic` for ``is_staff`` or ``group`` based permission logic as well.


Customize permission logic
--------------------------

Your own permission logic class must be a subclass of :class:`permission.logics.base.PermissionLogic` and must override
``has_perm(user_obj, perm, obj=None)`` method which return boolean value.
