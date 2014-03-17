"""
Use cases that this script will implement:

1.   Search concepts by keyword and iterate through the results.
2.   Interpret header response from a concept search.
3a.  Retrieve one snomed concept by code.
3b.  Search concepts by code with filter.
4.   Search collections by keyword filtered by owner and access type.
5.   Retrieve all concepts in a collection.
6.   Search sources by keyword sorted by name description and showing 2
     pages w/ 20 results per page.
7.   Search concepts updated since my last dictionary sync.
8.   Search collections by concept.
9.   List all sources sorted by name.
10.  List all resources in the OCL API
11.  List possible fields for a collection object.
12.  Add / remove a star for my user to a collection.
13.  Create new collection named "My Collection" form selected concepts
     as private.
14.  View collection meta data and concepts.
15a. Edit collection metadata.
15b. Add preferred Spanish name to a collection
16.  Add selected concepts to collection.
17.  Change “My Collection” to publicly editable.
18.  Remove selected concepts from collection.
19.  Export results of concept search as CSV with SNOMED mappings and
     preferred English name.
20a. Use API to get the intersection of concepts from “My Collection” and
     # the “MCL Core Concepts”
20b. Use python objects to get the intersection of concepts from “My
     Collection” and the “MCL Core Concepts”
"""


################################################################################
# COMMON CODE - Run at the beginning of each code block
################################################################################

import ocl_api_resources
import requests
import simplejson as json

api_url_root = 'http://staging.openconceptlab.org/rest/v1/'


################################################################################
# 1. Search concepts by keyword and iterate through the results.
#
# GET /rest/v1/concepts/?q={search_criteria}
################################################################################

curl_url = api_url_root + 'concepts/'
curl_param = {
    'q': 'cough'
}
r = requests.get(curl_url, params=curl_param)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 2. Display header response from a concept search.
#
# GET /rest/v1/concepts/?q={search_criteria}
################################################################################

from pprint import pprint

curl_url = api_url_root + 'concepts/'
curl_param = {
    'q': 'cough'
}
r = requests.get(curl_url, params=curl_param)
pprint r.headers


################################################################################
# 3a. Retrieve one snomed concept by code.
#
# GET /rest/v1/sources/{source_id}/concepts/{concept_id}
################################################################################

curl_url = api_url_root + 'sources/snomed/concepts/49727002'
r = requests.get(curl_url)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 3b. Search for concept by code with filter.
#
# GET /rest/v1/concepts/?q={search_criteria}&class={class}
################################################################################

curl_url = api_url_root + 'concepts/'
curl_param = {
    'q': '49727002',
    'class': 'Diagnosis'
}
r = requests.get(curl_url, params=curl_param)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 4. Search collections by keyword filtered by owner and access type.
#
# GET /rest/v1/collections/?q={search_criteria}&owner={username}&access={access_type}
################################################################################

curl_url = api_url_root + 'collections/'
curl_param = {
    'q': 'antenatal',
    'owner': 'paynejd',
    'access': 'public'
}
r = requests.get(curl_url, params=curl_param)
collections = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in collections:
    print c + "\n"


################################################################################
# 5. Retrieve all concepts in a collection.
#
# GET /rest/v1/concepts/?collection={collection_id}
################################################################################

collection_uuid = '3101BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
curl_url = api_url_root + 'concepts/'
curl_param = {
    'collection': collection_uuid
}
r = requests.get(curl_url, params=curl_param)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 6. Search collections by keyword reverse sorted by name and showing page 2
# with 15 results per page.
#
# GET /rest/v1/collections/?q={criteria}&sortDesc={field}&count={#}&startIndex={#}
################################################################################

curl_url = api_url_root + 'collections/'
curl_param = {
    'q': 'antenatal',
    'sortDesc': 'display',
    'count': 15,
    'startIndex': 15
}
r = requests.get(curl_url, params=curl_param)
collections = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in collections:
    print c + "\n"


################################################################################
# 7. Search concepts updated since my last dictionary sync.
#
# GET /rest/v1/concepts/?updatedSince={lastUpdatedDate}
################################################################################

last_sync = '2013-04-22T14:26:15Z'
curl_url = api_url_root + 'concepts/'
curl_param = {
    'updatedSince': last_sync
}
r = requests.get(curl_url, params=curl_param)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 8. Search collections by concept.
#
# GET /rest/v1/collections/?concept={concept_id}
################################################################################

concept_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
curl_url = api_url_root + 'collections/'
curl_param = {
    'concept': concept_uuid
}
r = requests.get(curl_url, params=curl_param)
collections = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in collections:
    print c + "\n"


################################################################################
# 9. List all sources sorted by name.
#
# GET /rest/v1/sources/?sortAsc={field}
################################################################################

curl_url = api_url_root + 'sources/'
curl_param = {
    'sortAsc': 'display'
}
r = requests.get(curl_url, params=curl_param)
sources = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for s in sources:
    print s + "\n"


################################################################################
# 10. List all resources in the OCL API
#
# GET /rest/v1/catalog/
################################################################################

curl_url = api_url_root + 'catalog/'
r = requests.get(curl_url)
print r.text


################################################################################
# 11. List possible fields for a collection object.
#
# GET /rest/v1/catalog/collections/
################################################################################

curl_url = api_url_root + 'catalog/collections/'
r = requests.get(curl_url)
print r.text


################################################################################
# 12. Add / remove a star for my user to a collection.
#
# POST /rest/v1/stars
# Body content:
# { "resourceType":"concept", "resourceUuid":"uuid", "username": "paynejd" }
#
# Note: username is needed only if modifying a star for a user other than
# the authenticated user, which is generally not allowed.
################################################################################

payload = {
    "resourceType": "collection",
    "resourceUuid": "bwhefw82-ur2usdmf-ndefwee"
}
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'stars/'
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 13. Create new collection named "My Collection" form selected concepts as
# private.
#
# POST /rest/v1/collections
# Body content:
# { "names": [],
#   "descriptions": [],
#   "collectionType": "Collection",
#   "owner": {username},
#   "publicAccess": "View",
#   "concepts": []
# }
################################################################################

payload = {
    "names": [
        {
            "name": "Oncology Diagnosis Starter Set",
            "locale": "en",
            "preferred": true
        }
    ],
    "descriptions": [
        {
            "description": "Basic facility-based diagnostic terminology starter set",
            "locale": "en",
            "preferred": true
        }
    ],
    "collectionType": "Collection",
    "owner": "jdoe",
    "publicAccess": "View",
    "concepts": [
        { "uuid": "0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f" },
        { "uuid": "11de-8d13-0010c6dffd0f0010c6df-fd0f-c2cc" }
    ]
}
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/'
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 14. View all metadata for a collection (including list of concept references).
#
# GET /rest/v1/collections/{uuid}/?fields={field_list}
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
curl_url = api_url_root + 'collections/'
curl_param = {
    'fields': '*'
}
r = requests.get(curl_url, params=curl_param)
print r.text


################################################################################
# 15a. Update collection metadata.
#
# POST /rest/v1/collections/{uuid}
# Body content:
# {   "names": [],
#     "descriptions": [],
#     "collectionType": "Collection",
#     "publicAccess": "View",
#     "concepts": []
# }
#
# The above fields are illustrative. Refer to the documentation for a full
# description of available fields.
#
# Note that POST only writes to fields that are included in the body of the
# request, other fields remain unchanged unless automatically updated by the
# system (e.g. auditing info). Updating a sub-resource through the parent
# resource overwrites list. For example, a POST to the "names" field of a
# collection will replace all names with those provided. Use the sub-resource
# URL to add/modify/delete a single name. For example, to add a name:
#
#     POST /rest/v1/collections/{uuid}/names
#     Body content: { "name":"Mi Nombre", "locale":"es", "preferred":false }
#
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
payload = {
    "names": [
        {
            "name": "Oncology Diagnosis Starter Set",
            "locale": "en",
            "preferred": true
        }
    ],
    "descriptions": [
        {
            "description": "Basic facility-based diagnostic terminology starter set",
            "locale": "en",
            "preferred": true
        }
    ],
    "collectionType": "Collection",
    "owner": "jdoe",
    "publicAccess": "View",
    "concepts": [
        { "uuid": "0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f" },
        { "uuid": "11de-8d13-0010c6dffd0f0010c6df-fd0f-c2cc" }
    ]
}
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/' + collection_uuid + "/"
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 15b. Add preferred Spanish name to a collection
#
# POST /rest/v1/collections/{uuid}/names/
# Body content:
# {  "name": "atencion prenatal",
#    "locale": "es",
#    "preferred": true
# }
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
payload = {
    "name": "Atencion Prenatal",
    "locale": "es",
    "preferred": true
}
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/' + collection_uuid + "/names/"
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 16. Add selected concepts to collection.
#
# POST /rest/v1/collections/{uuid}/concepts/
# Body content:
# [ { "uuid": {uuid} }, { "source":{source"}, "conceptId":{conceptId} } ]
#
# (??) What formats are supported for representing concepts?
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
payload = [
    {
        "uuid": "8d492ee0-c2cc-11de-8d13-0010c6dffd0f"
    },
    {
        "source": "ciel",
        "conceptId": "1234"
    }
]
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/' + collection_uuid + "/concepts/"
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 17. Change “My Collection” to publicly editable.
#
# POST /rest/v1/collections/{uuid}
# Body content:
# { "publicAccess":"Edit" }
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
payload = {
    "publicAccess": "Edit"
}
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/' + collection_uuid + "/"
r = requests.post(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 18. Remove selected concepts from collection.
#
# DELETE /rest/v1/collections/{uuid}/concepts
# Body content:
# [ { "uuid": {uuid} }, { "source":{source"}, "conceptId":{conceptId} } ]
#
# (??) What formats are supported for representing concepts?
################################################################################

collection_uuid = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
payload = [
    {
        "uuid": "8d492ee0-c2cc-11de-8d13-0010c6dffd0f"
    },
    {
        "source": "ciel",
        "conceptId": "1234"
    }
]
username = 'jdoe'
password = 'mypass'
curl_url = api_url_root + 'collections/' + collection_uuid + "/concepts/"
r = requests.delete(curl_url, data=payload, auth=(username, password))
print "Response Status Code: " + r.status_code + "\n"
r.raise_for_status()


################################################################################
# 19. Get results of concept search as CSV with only uuid, preferred name,
# locale of preferred name, and SNOMED mappings.
#
# GET /rest/v1/concepts/?q={search_criteria}&fields={field_list}&format={format}
#
# (??) Format for fields?
# (??) Change the format to CSV in the request header
################################################################################

curl_url = api_url_root + 'concepts/'
curl_param = {
    'q': 'cough',
    'fields': 'uuid,display,display_locale,mappings:snomed',
    'format': 'csv'
}
r = requests.get(curl_url, params=curl_param)
print r.text


################################################################################
# 20a. Use API to get the intersection of concepts from “My Collection” and
# the “MCL Core Concepts”
#
# GET /rest/v1/concepts/?intersect={uuid_1},{uuid_2}(,...)
#
# (??) Treat intersection as a parameter?
################################################################################

collection_uuid_1 = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
collection_uuid_2 = '3101BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
curl_url = api_url_root + 'concepts/'
curl_param = {
    'intersect': collection_uuid_1 + ',' + collection_uuid_2
}
r = requests.get(curl_url, params=curl_param)
concepts = json.loads(r.text, object_hook=ocl_api_resources.object_hooker)
for c in concepts:
    print c + "\n"


################################################################################
# 20b. Use python objects to get the intersection of concepts from “My
# Collection” and the “MCL Core Concepts”
#
# GET /rest/v1/collections/{uuid}/
################################################################################

collection_uuid_1 = '0010c6dffd0f-c2cc-11de-8d13-0010c6dffd0f'
collection_uuid_2 = '3101BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
curl_url_1 = api_url_root + 'collections/' + collection_uuid_1
curl_url_2 = api_url_root + 'collections/' + collection_uuid_2
curl_param = {
    'fields': '*'
}
r1 = requests.get(curl_url_1, params=curl_param)
r2 = requests.get(curl_url_2, params=curl_param)
coll_1 = json.loads(r1.text, object_hook=ocl_api_resources.object_hooker)
coll_2 = json.loads(r2.text, object_hook=ocl_api_resources.object_hooker)
coll_intersect = coll_1.intersect(coll_2)
for c in coll_intersect.concepts:
    print "(" + c.source + ":" + c.conceptId + ") " + c.display + " [" + c.display_locale + "]\n"


