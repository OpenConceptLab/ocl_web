import simplejson as json


class ApiResource(object):

    def __init__(self):
        self.uuid = ""
        self.url = ""
        self.display = ""
        self.display_locale = ""
        self.retired = ""
        self.properties = {}
        self.auditInfo = {}
        self.resourceVersion = ""

    def set_values(self, dct):
        # validate values??
        for key, value in dct.iteritems():
            # print key, value
            # raw_input()
            self.__setattr__(key, value)

    def json(self):
        return json.dumps(
            dict(self.__dict__.items() + {'__type__': self.__class__.__name__}.items()))

    def __repr__(self):
        return '(' + self.uuid + ') ' + self.display + ' [' + self.display_locale + ']'


def object_hooker(dct):
    class_names = {
        'OclMapType': MapType,
        'OclConcept': Concept,
        'OclConceptClass': ConceptClass,
        'OclConceptDataType': ConceptDataType,
        'OclCollection': Collection,
        'OclMapping': Mapping,
        'OclSource': Source,
        'OclStar': Star,
        'OclUser': User
    }
    if '__type__' in dct:
        class_name = dct['__type__']
        try:
            # Instantiate class based on value in the variable
            x = class_names[class_name]()
            x.set_values(dct)
            return x
        except KeyError:
            # handle error - Class is not defined
            pass
    return dct
