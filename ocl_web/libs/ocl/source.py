from ..ocl import ApiResource


class Source(ApiResource):

    def __init__(self):
        super(Source, self).__init__()
        self.shortCode = ""
        self.names = {}
        self.descriptions = ""
        self.sourceType = ""
        self.owner = ""
        self.publicAccess = ""
        self.sharedUsers = []
        self.starCount = 0

    def get_preferred_name(self, locale='en'):
        pass

    def __repr__(self):
        return '(' + self.shortCode + ') ' + self.display + ' [' + self.display_locale + ']'
