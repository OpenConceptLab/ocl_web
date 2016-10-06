class SearchStringFormatter:
    @staticmethod
    def add_wildcard(request):
        if not request.GET._mutable:
            request.GET._mutable = True

        if request.GET.get('q') and not request.GET.get('exact_match'):
            request.GET['q'] = "*" + request.GET['q'] + "*"
