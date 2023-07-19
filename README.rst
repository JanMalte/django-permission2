django-permission2
==========================
.. image:: https://img.shields.io/pypi/v/django-permission2.svg?style=flat-square
    :target: https://github.com/janmalte/django-permission2/blob/master/setup.py
    :alt: Version
.. image:: https://img.shields.io/pypi/l/django-permission2.svg?style=flat-square
    :target: https://github.com/janmalte/django-permission2/blob/master/LICENSE
    :alt: License
.. image:: https://img.shields.io/pypi/format/django-permission2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-permission2/
    :alt: Format
.. image:: https://img.shields.io/pypi/pyversions/django-permission2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-permission2/
    :alt: Supported python versions
.. image:: https://img.shields.io/pypi/status/django-permission2.svg?style=flat-square
    :target: https://pypi.python.org/pypi/django-permission2/
    :alt: Status
.. image:: https://readthedocs.org/projects/django-permission2/badge/?version=latest
    :target: https://django-permission2.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. image:: https://github.com/JanMalte/django-permission2/actions/workflows/run-tests.yml/badge.svg
    :target: https://github.com/JanMalte/django-permission2/actions/workflows/run-tests.yml
    :alt: tests

Author
    Malte Gerth <mail@malte-gerth.de>
Original Author
    Alisue <lambdalisue@hashnote.net>
Supported python versions
    Python 3.8, 3.9, 3.10
Supported django versions
    Django 2.2, 3.2, 4.0, 4.1

An enhanced permission library which enables a *logic-based permission system*
to handle complex permissions in Django.


Documentation
-------------
http://django-permission2.readthedocs.org/

Installation
------------
Use pip_ like::

    $ pip install django-permission2

.. _pip:  https://pypi.python.org/pypi/pip


Usage
-----

The following might help you to understand as well.

- Basic strategy or so on, `Issue #28 <https://github.com/jazzband/django-permission/issues/28>`_
- Advanced usage and examples, `Issue #26 <https://github.com/jazzband/django-permission/issues/26>`_

Configuration
~~~~~~~~~~~~~
1.  Add ``permission`` to the ``INSTALLED_APPS`` in your settings
    module

    .. code:: python

        INSTALLED_APPS = (
            # ...
            'permission',
        )

2.  Add our extra authorization/authentication backend

    .. code:: python

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend', # default
            'permission.backends.PermissionBackend',
        )

3.  Follow the instructions below to apply logical permissions to django models

Quick tutorial
~~~~~~~~~~~~~~

Let's assume you wrote an article model which has an ``author`` attribute to store the creator of the article, and you want to give that author full control permissions
(e.g. add, change and delete permissions).

1.  Add ``import permission; permission.autodiscover()`` to your ``urls.py`` like:

    .. code:: python

        from django.conf.urls import patterns, include
        from django.urls import path
        from django.contrib import admin

        admin.autodiscover()

        # only add the following line
        import permission; permission.autodiscover()

        urlpatterns = [
            path('admin/', include(admin.site.urls)),
            # ...
        ]

2.  Write ``perms.py`` in your application directory like:

    .. code:: python

        from permission.logics import AuthorPermissionLogic
        from permission.logics import CollaboratorsPermissionLogic

        PERMISSION_LOGICS = (
            ('your_app.Article', AuthorPermissionLogic()),
            ('your_app.Article', CollaboratorsPermissionLogic()),
        )

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

    # You have to apply 'permission.add_article' to users manually because it
    # is not an object permission.
    from permission.utils.permissions import perm_to_permission
    user1.user_permissions.add(perm_to_permission('permission.add_article'))

    assert user1.has_perm('permission.add_article') == True
    assert user1.has_perm('permission.change_article') == False
    assert user1.has_perm('permission.change_article', art1) == True
    assert user1.has_perm('permission.change_article', art2) == False

    assert user2.has_perm('permission.add_article') == False
    assert user2.has_perm('permission.delete_article') == False
    assert user2.has_perm('permission.delete_article', art1) == False
    assert user2.has_perm('permission.delete_article', art2) == True

License
-------------------------------------------------------------------------------
The MIT License (MIT)

Copyright (c) 2022 Malte Gerth <mail@malte-gerth.de>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
