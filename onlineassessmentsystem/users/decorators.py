from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

def student_required(function = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = '/users/login'):
    '''
    Custom Decorator that is used to authorise the user as Student.
    '''
    actual_decorator = user_passes_test(
        lambda user : user.is_active and user.isStudent,
        login_url = login_url,
        redirect_field_name = redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

def faculty_required(function = None, redirect_field_name = REDIRECT_FIELD_NAME, login_url = '/users/accessDenied'):
    '''
    Custom Decorator that is used to authorise the user as Student.
    '''
    actual_decorator = user_passes_test(
        lambda user : user.is_active and not user.isStudent,
        login_url = login_url,
        redirect_field_name = redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator