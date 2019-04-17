from unittest import TestCase
from apps.core.utils import SearchStringFormatter
from django.http import QueryDict


class FakeRequest(object):
    """ FakeRequest class """
    def __init__(self, _dict):
        self.GET = _dict


class SearchStringFormatterTests(TestCase):
    def test_add_wildcard_without_exact_match(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(**{'q': 'some search phrase', 'exact_match': False})
        query_dict._mutable = False
        request = FakeRequest(query_dict)

        SearchStringFormatter.add_wildcard(request)

        self.assertEquals(request.GET['q'], 'some* search* phrase*')

    def test_add_wildcard_with_exact_match(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(**{'q': 'some search phrase', 'exact_match': True})
        query_dict._mutable = False
        request = FakeRequest(query_dict)

        SearchStringFormatter.add_wildcard(request)

        self.assertEquals(request.GET['q'], 'some search phrase')

    def test_add_wildcard_with_empty_query_string(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(**{'q': '', 'exact_match': False})
        query_dict._mutable = False
        request = FakeRequest(query_dict)

        SearchStringFormatter.add_wildcard(request)

        self.assertEquals(request.GET['q'], '')

    def test_add_wildcard_without_query_string(self):
        query_dict = QueryDict('', mutable=True)
        query_dict.update(**{'exact_match': False})
        query_dict._mutable = False
        request = FakeRequest(query_dict)

        SearchStringFormatter.add_wildcard(request)

        self.assertTrue('q' not in request.GET)
