
import types
try:
    from django.urls.resolvers import URLPattern as DjangoRegexURLPattern
    from django.urls import URLResolver as DjangoRegexURLResolver
except ImportError: # Django<2.0
    from django.core.urlresolvers import (
        RegexURLPattern as DjangoRegexURLPattern,
        RegexURLResolver as DjangoRegexURLResolver
    )
from urldecorators.helpers import func_from_callable


__all__ = ["RegexURLResolver", "RegexURLPattern"]


class DecoratorMixin(object):
    """
    A mixin which adds support for decorating all resolved views
    """
    
    def __init__(self, *args, **kwargs):
        super(DecoratorMixin, self).__init__(*args, **kwargs)
        self.decorators = []
    
    def resolve(self, path):
        match = super(DecoratorMixin, self).resolve(path)
        if not match:
            return match
        match.func = self.apply_decorators(match.func)
        return match
    
    def apply_decorators(self, callback):
        if not isinstance(callback, types.FunctionType):
            # Lots of decorators tries to update_wrapper which can fail when view
            # is a callable class or class method. So give them standard function.
            callback = func_from_callable(callback)
        for decorator in self.decorators:
            callback = decorator(callback)
        return callback


class RegexURLPattern(DecoratorMixin, DjangoRegexURLPattern):
    """
    Django RegexURLPattern with support for decorating resolved views
    """


class RegexURLResolver(DecoratorMixin, DjangoRegexURLResolver):
    """
    Django RegexURLResolver with support for decorating resolved views
    """

