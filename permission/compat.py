add_to_builtins = None

try:
    # django.utils.importlib is removed from Django 1.9
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module


def is_authenticated(user_obj):
    return user_obj.is_authenticated


def is_anonyomus(user_obj):
    return user_obj.is_anonymous


try:
    # Django 1.7 or over use the new application loading system
    from django.apps import apps

    get_model = apps.get_model
except ImportError:
    pass

try:
    from django.utils.module_loading import import_string
except ImportError:
    try:
        from django.utils.module_loading import import_by_path as import_string
    except ImportError:

        def import_string(dotted_path):
            try:
                module_path, class_name = dotted_path.rsplit(".", 1)
            except ValueError:
                raise ImportError(f"{dotted_path} doesn't look like a module path")
            module = import_module(module_path)
            try:
                return getattr(module, class_name)
            except AttributeError:
                raise ImportError(f'Module "{module_path}" does not define a "{class_name}" attribute/class')


try:
    # Python 3
    from urllib.parse import urlparse
except ImportError:
    # Python 2
    pass


def isstr(x):
    return isinstance(x, str)
