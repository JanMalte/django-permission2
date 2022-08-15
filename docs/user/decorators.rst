Decorators
==========

Class, method, or function decorator
-------------------------------------
Like Django's ``permission_required`` but it can be used for object permissions
and as a class, method, or function decorator.
Also, you don't need to specify a object to this decorator for object permission.
This decorator automatically determined the object from request
(so you cannnot use this decorator for non view class/method/function but you
anyway use ``user.has_perm`` in that case).


.. code:: python

    >>> from permission.decorators import permission_required
    >>> # As class decorator
    >>> @permission_required('auth.change_user')
    >>> class UpdateAuthUserView(UpdateView):
    ...     pass
    >>> # As method decorator
    >>> class UpdateAuthUserView(UpdateView):
    ...     @permission_required('auth.change_user')
    ...     def dispatch(self, request, *args, **kwargs):
    ...         pass
    >>> # As function decorator
    >>> @permission_required('auth.change_user')
    >>> def update_auth_user(request, *args, **kwargs):
    ...     pass
