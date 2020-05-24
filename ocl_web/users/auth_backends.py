from allauth.account import app_settings
from allauth.account.auth_backends import AuthenticationBackend

from libs.ocl import OclApi
from users.models import User


class APIAuthenticationBackend(AuthenticationBackend):
    def get_user(self, user_id):
        return User(username=user_id)

    def _authenticate_by_username(self, **credentials):
        username_field = app_settings.USER_MODEL_USERNAME_FIELD
        if not username_field:
            return None
        return self._authenticate(username=credentials.get(username_field), password=credentials.get('password'))

    def _authenticate_by_email(self, **credentials):
        email = credentials.get('email', credentials.get('username'))
        return self._authenticate(username=email, password=credentials.get('password'))

    @staticmethod
    def _authenticate(username=None, password=None):
        ocl = OclApi()

        def authenticate_with_api(_username, _password, hashed=True):
            api_response = ocl.get_user_auth(_username, _password, hashed=hashed)

            if api_response.status_code == 200:
                _user = User(username=username)
                _user.ocl_api_token_object = api_response.json()
                return _user
            return None

        result = authenticate_with_api(username, password, hashed=False)
        if result:
            return result
        else:
            # try to fallback to existing user with hashed password
            try:
                user = User.objects.get(username=username)
                result = authenticate_with_api(user.username, user.password)
                if result:
                    return result
            except User.DoesNotExist:
                pass

        return None
