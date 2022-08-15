Templatetags
============

Override the builtin ``if`` template tag
----------------------------------------
django-permission2 overrides the builtin ``if`` tag, adding two operators to handle
permissions in templates.
You can write a permission test by using ``has`` keyword, and a target object with ``of`` as below.


.. code:: html

    {% if user has 'blogs.add_article' %}
        <p>This user have 'blogs.add_article' permission</p>
    {% elif user has 'blog.change_article' of object %}
        <p>This user have 'blogs.change_article' permission of {{object}}</p>
    {% endif %}

    {# If you set 'PERMISSION_REPLACE_BUILTIN_IF = False' in settings #}
    {% permission user has 'blogs.add_article' %}
        <p>This user have 'blogs.add_article' permission</p>
    {% elpermission user has 'blog.change_article' of object %}
        <p>This user have 'blogs.change_article' permission of {{object}}</p>
    {% endpermission %}

.. note::
    You have to add `'permission.templatetags.permissionif'` to `'builtins'` option manually.
    See
    - https://docs.djangoproject.com/en/1.9/releases/1.9/#django-template-base-add-to-builtins-is-removed
    - https://docs.djangoproject.com/en/1.9/topics/templates/#module-django.template.backends.django
    Or following example:

    .. code:: python

        TEMPLATES = [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'builtins': ['permission.templatetags.permissionif'],
                },
            },
        ]
