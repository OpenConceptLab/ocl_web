"""
    Signal handlers to interface with the django-allauth package.
"""

from libs.ocl import OclApi


def email_confirmed_handler(sender, request, email_address, **kwargs):
    """
    Signal handler called when a user logged into the web app.

    One idea is to retrieve the backend auth token and save it in the web
    app for subsequent access, but we do not have easy access to the
    django user object.
    """
    print 'Email Confirmed signal for ', request.user.username


def user_logged_in_handler(sender, request, user, **kwargs):
    """
    Signal handler called when a user logged into the web app.
    We need to retrieve the backend auth token for subsequent access.
    The token is saved in the session.

    Ideally, we would have handled this in the authentication backend, but this version of Django
    doesn't pass a request object to the `users.auth_backend.APIAuthenticationBackend.authenticate` method.
    The first version that does is 1.11(https://docs.djangoproject.com/en/3.0/releases/1.11/).
    """
    ocl = OclApi()
    ocl.save_auth_token(request, user.ocl_api_token_object)


def user_password_reset_handler(sender, request, user, **kwargs):
    ocl = OclApi(admin=True, debug=True)
    result = ocl.sync_password(user)
    if result.status_code == 200:
        result = ocl.get_user_auth(user.username, user.password)
        if result.status_code == 200:
            ocl.save_auth_token(request, result.json())
