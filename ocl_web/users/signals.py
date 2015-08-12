"""
    Signal handlers to interface with the django-allauth package.

    Tie the front end user models with the backend, each front end
    user has a correponding entry in the API database.
"""
from libs.ocl import OclApi


def user_created_handler(sender, request, user, **kwargs):
    """
    Signal handler called when a new user is created, so that we can create
    a corresponding user at the backend.
    """
    print 'user created handler %s' % user.username
    ocl = OclApi(admin=True, debug=True)
    data = {
        'username': user.username,
        'email': user.email,
        'hashed_password': user.password,
        'name': '%s %s' % (user.first_name, user.last_name),  # not great
    }
    result = ocl.create_user(data)
    print result.status_code
    if result.status_code == 201:
        # result.json() has data
        pass

    elif result.status_code == 400:
        # try reactivate for now, this is very not secure, #TODO
        result = ocl.reactivate_user(user.username)
        if result == 204:
            print 'reactivated'


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

    TODO: Cannot get to, or hashed_password is not saved, so this
    fails with an invalid password.
    """
    print 'User logged in Signal for:', user.username
    ocl = OclApi(admin=True, debug=True)
    result = ocl.get_user_auth(user.username, user.password)
    if result.status_code == 200:
        print 'LOGIN auth code:', result.json()
        ocl.save_auth_token(request, result.json())


