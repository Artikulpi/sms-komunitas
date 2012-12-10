from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings

def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url=None):
    """
    Decorator for views that checks if current user have is_staff permission
    """
    if login_url==None:
        login_url = settings.LOGIN_URL
    
    actual_decorator = user_passes_test(
        lambda u: u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def admin_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                    login_url=None):
    """
    Decorator for views that checks if current user have is_superuser permission
    """
    if login_url==None:
        login_url = settings.LOGIN_URL
    
    actual_decorator = user_passes_test(
        lambda u: u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
