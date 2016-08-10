from unittest import TestCase
from mock import Mock, patch, mock
from views import UserDetailView
from libs.ocl import OclApi

class MyDict(dict):
    def __init__(self,name):
        self.username = name

class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self):
        self.session = {}
        self.GET = {}
        self.user = MyDict('tempuser')

class FakeResponse(object):
    """ FakeRequest class """
    def __init__(self,data):
        self.session = {}
        self.GET = {}
        self.detail = data
    def json(self):
        return {'detail': self.detail}

class UserDetailViewTest(TestCase):

    @patch('libs.ocl.OclApi.get')
    def test_getContextData_contextDataReceivedAndSet(self, mock_get):

        user = FakeResponse('user')
        org = FakeResponse('org')
        src = FakeResponse('src')
        col = FakeResponse('col')

        mock_get.side_effect = [user, org, src, col]

        userDetailView = UserDetailView()
        userDetailView.object = ''
        userDetailView.request = FakeRequest()
        kwargs = {'object':MyDict('Jon')}
        context = userDetailView.get_context_data(**kwargs)
        self.assertEquals(context['ocl_user'],user.json())
        self.assertEquals(context['orgs'], org.json())
        self.assertEquals(context['sources'], src.json())
        self.assertEquals(context['collections'], col.json())