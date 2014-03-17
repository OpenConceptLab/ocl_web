from ..ocl import ApiResource


class ConceptDataType(ApiResource):

    def __init__(self):
        super(ConceptDataType, self).__init__()
        self.names = []
        self.descriptions = []
        self.sources = []
