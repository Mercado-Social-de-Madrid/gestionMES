from django.contrib.admin.views.decorators import user_passes_test

def superuser_required(view_func=None, login_url='dashboard'):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name='permission'
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator