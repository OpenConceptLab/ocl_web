from ..ocl import ApiResource


class Star(ApiResource):
    def __init__(self):
        super(Star, self).__init__()
        self.resource = {}
        self.username = ""
        self.dateStarred = ""
