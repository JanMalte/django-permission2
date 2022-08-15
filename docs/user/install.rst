Installation
============

.. _`install`:

Installing django-permission2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Install latest stable version into your python environment using pip::

    pip install django-permission2

2. Once installed add ``permission`` to your ``INSTALLED_APPS`` in settings.py::

    .. code:: python

        INSTALLED_APPS = (
            ...
            'permission',
        )

3.  Add our extra authorization/authentication backend

    .. code:: python

        AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend', # default
            'permission.backends.PermissionBackend',
        )

4.  Follow the instructions below to apply logical permissions to django models

Autodiscovery
~~~~~~~~~~~~~
Like django's admin package, django-permission2 automatically discovers the ``perms.py`` in your application directory **by running ``permission.autodiscover()``**.
Additionally, if the ``perms.py`` module has a ``PERMISSION_LOGICS`` variable, django-permission2 automatically run the following functions to apply the permission logics.

.. code:: python

    for model, permission_logic_instance in PERMISSION_LOGICS:
        if isinstance(model, str):
            model = get_model(*model.split(".", 1))
        add_permission_logic(model, permission_logic_instance)

.. note::

    Autodiscover feature is automatically called. To disable, use `PERMISSION_AUTODISCOVER_ENABLE` setting.
