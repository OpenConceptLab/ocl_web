from api_resource import ApiResource
from collection import Collection
from concept import Concept
from concept_class import ConceptClass
from concept_data_type import ConceptDataType
from concept_list import ConceptList
from map_type import MapType
from mapping import Mapping
from source import Source
from star import Star
from user import User


def object_hooker(dct):
    class_names = {
        'OclMapType': MapType,
        'OclConcept': Concept,
        'OclConceptClass': ConceptClass,
        'OclConceptList': ConceptList,
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
