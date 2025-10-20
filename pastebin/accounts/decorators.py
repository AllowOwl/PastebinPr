from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import user_passes_test


def admin_required(view_func):
    def check_admin(user):
        return user.is_authenticated and user.is_admin()
    
    return user_passes_test(check_admin)(view_func)

def moderator_required(view_func):
    def check_moderator(user):
        return user.is_authenticated and (user.is_moderator() or user.is_admin())
    
    return user_passes_test(check_moderator)(view_func)

def user_required(view_func):
    def check_user(user):
        return user.is_authenticated
    
    return user_passes_test(check_user)(view_func)
