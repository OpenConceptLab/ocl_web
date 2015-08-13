# from ..ocl import ApiResource


# class Concept(ApiResource):
#     def __init__(self):
#         super(Concept, self).__init__()
#         self.conceptId = ""
#         self.source = ""
#         self.names = []
#         self.descriptions = []
#         self.datatype = ""
#         self.classtype = ""
#         self.answers = []
#         self.questions = []
#         self.isSet = False
#         self.setMembers = []
#         self.mappings = []
#         self.collections = []
#         self.starCount = 0

#     def __repr__(self):
#         return '(' + self.source + ':' + self.conceptId + ') ' + self.display + ' [' + self.display_locale + ']'

#     def getPreferredName(self, locale='en'):
#         # If locale is a string, return the first preferred name for the specified locale.
#         # If locale is a list, then check for preferred names in the specified locale order.
#         # If no preferred name is set for any of the specified locales, use the first
#         # non-preferred name based on the order of locales specified.
#         # If still no match, return the first preferred name of a non-specified locale.
#         # If still no match, return the first non-preferred name of a non-specified locale.
#         # If no match at all, return None.

#         # Return the first preferred name for the specified locale
#         for name in self.names:
#             if name.locale == locale and name.preferred:
#                 return name
#         # If not set, return the first non-preferred name for the specified locale

#         # If does not exist, return the first
#         return None
