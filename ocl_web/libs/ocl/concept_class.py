from ..ocl import ApiResource


class ConceptClass(ApiResource):
    def __init__(self):
        super(ConceptClass, self).__init__()
        self.names = []
        self.descriptions = []
        self.sources = []
