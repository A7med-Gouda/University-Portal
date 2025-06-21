from rest_framework.request import HttpRequest
from django.http import Http404

def IsAuth(request):
    if request.user.is_authenticated:
        return True
    else:
        return False

def has_permission(codename: str, request: HttpRequest) -> bool:
    
    user = request.user
    
    user_permissions = user.get_all_permissions()
    
    if codename in user_permissions:
        return True

    return False


def _get_queryset(klass):

    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, "_default_manager"):
        return klass._default_manager.all()
    return klass

def get_object_or_404(klass, error="This Object not founded yet 404",*args, **kwargs):

    queryset = _get_queryset(klass)
    if not hasattr(queryset, "get"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to get_object_or_404() must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        raise Http404(
            error
        )
