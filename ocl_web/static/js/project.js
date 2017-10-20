/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', ['ui.bootstrap']);

/* Add CSRF token for the web site. Note that we are setting the common defaults
 instead of post, because we need it for delete as well?
 */
app.config(function ($httpProvider, $interpolateProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
});

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

function make_url(location, path) {
    var url = location.protocol() + '://' + location.host() + ':' + location.port() + path;
    return path;
}

/* Make a url using a base URL, but take care to remove the debug flag and other arguments
 when presence.
 */
function make_sub_url(location, sub_path) {
    var parts = URI.parse(location);
    parts['query'] = null;
    parts['path'] += sub_path;
    var u = URI.build(parts);
    return u.toString();
}

function set_debug(loc, scope) {
    var debug = new URI(loc.absUrl()).hasQuery('debug', true);
    scope.debug = debug;

}

function locale_by_name(locale_choices, n) {
    for (var i = 0; i < locale_choices.length; i++) {
        if (locale_choices[i].name == n) {
            return locale_choices[i];
        }
    }
};

function locale_by_code(locale_choices, c) {
    for (var i = 0; i < locale_choices.length; i++) {
        if (locale_choices[i].code == c) {
            return locale_choices[i];
        }
    }
};


/* Make a controller that access concept attributes, supporting CRUD operations.
 This works for most concept items like names and descriptions.

 :param a_url_part: is the REST item name string, e.g. "names"
 :param a_field_names: is a list of field names that we will copy from the frontend
 to the back end in create and update calls.
 :param a_item_key: specifies the field name in the item object used to uniquely
 identify the object to the backend.
 */
function makeController(a_url_part, a_field_names, a_item_key) {

    return function conceptItemController($scope, $http, $location) {

        var url_part = a_url_part; // from makeController
        var field_names = a_field_names;
        var item_key = a_item_key || 'uuid';

        $scope.isCreatingItem = false;
        $scope.isEditingItem = false;
        $scope.editedItem = null;
        $scope.item = null;
        $scope.alerts = [];

        function resetCreateForm() {
            $scope.newItem = {};
        }

        function startCreatingItem() {
            $scope.isCreatingItem = true;
            $scope.isEditingItem = false;
            resetCreateForm();
        }

        function cancelCreatingItem() {
            $scope.isCreatingItem = false;
        }

        function startEditingItem() {
            $scope.isCreatingItem = false;
            $scope.isEditingItem = true;
        }

        function cancelEditingItem() {
            $scope.isEditingItem = false;
        }

        function shouldShowCreatingItem() {
            return !$scope.isEditingItem;
        }

        function shouldShowEditingItem() {
            return $scope.isEditingItem && !$scope.isCreatingItem;
        }

        function setEditedItem(item) {
            // Set the current edited object, copy otherwise Angular will update the real thing
            $scope.editedItem = angular.copy(item);

            // special case for locale, translate codes from API to display object for UI
            for (var i = 0; i < field_names.length; i++) {
                if ('locale' == field_names[i]) {
                    $scope.editedItem.locale = locale_by_code($scope.locale_choices, item.locale).name;
                }
                ;
            }
            ;
        };

        $scope.startCreatingItem = startCreatingItem;
        $scope.cancelCreatingItem = cancelCreatingItem;
        $scope.startEditingItem = startEditingItem;
        $scope.cancelEditingItem = cancelEditingItem;
        $scope.shouldShowCreatingItem = shouldShowCreatingItem;
        $scope.shouldShowEditingItem = shouldShowEditingItem;
        $scope.setEditedItem = setEditedItem;

        function loadItems() {

            var url = make_sub_url($location.absUrl(), url_part + '/');
            set_debug($location, $scope);

            $http.get(url)
                .success(function (data) {
                    $scope.item_list = data;
                });
        } // loadItems

        function loadLocales() {

            var url = $location.protocol() + '://' + $location.host() + ':' + $location.port() + '/core/options/locales/';
            $http.get(url)
                .success(function (data) {
                    $scope.locale_choices = data;
                });
        } // loadLocales

        function addItem(item) {

            // get form fields for API by name, specified
            // when controller is created.
            var data = {};
            for (var i = 0; i < field_names.length; i++) {
                fn = field_names[i];
                // special case for locale, translate text to code for API
                if ('locale' == fn) {
                    data[fn] = locale_by_name($scope.locale_choices, item[fn]).code;
                } else {
                    data[fn] = item[fn];
                }
                ;
            }

            var config = null;

            var url = $location.absUrl() + url_part + '/';
            $http.post(url, data, null)
                .success(function (data, status, headers, config) {
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    loadItems();
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });
                });

            resetCreateForm();
            cancelCreatingItem();
        } // addItem()

        $scope.addItem = addItem;

        function updateItem(item) {

            var data = {};
            for (var i = 0; i < field_names.length; i++) {
                fn = field_names[i];
                // special case for locale, translate text to code for API
                if ('locale' == fn) {
                    data[fn] = locale_by_name($scope.locale_choices, item[fn]).code;
                } else {
                    data[fn] = item[fn];
                }
                ;
            }
            ;
            var config = null;

            var url = $location.absUrl() + url_part + '/' + item[item_key] + '/';
            $http.post(url, data, null)
                .success(function (data, status, headers, config) {
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    loadItems();
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data.message);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });
                });

            $scope.editedItem = null;
            cancelEditingItem();
        } // updateItem

        $scope.updateItem = updateItem;

        function deleteItem(item) {

            var config = null;

            if (!confirm("Are you sure?")) {
                return;
            }
            console.log('DEL:' + item);
            var url = $location.absUrl() + url_part + '/' + item[item_key] + '/';
            $http.delete(url)
                .success(function (data, status, headers, config) {
                    console.log(data);
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    loadItems();
                })
                .error(function (data, status, headers, config) {
                    console.log('DEL error' + data);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });

                });
        } // deleteItem()

        $scope.deleteItem = deleteItem;

        $scope.closeAlert = function (index) {
            $scope.alerts.splice(index, 1);
        };

        loadItems();
        loadLocales();

    } // conceptItemController

} // makeController


// app.controller('ConceptDescriptionController', conceptItemController);
app.controller('ConceptDescriptionController', makeController('descriptions', ['description', 'description_type', 'external_id', 'locale', 'locale_preferred']));
app.controller('ConceptNameController', makeController('names', ['name', 'name_type', 'external_id', 'locale', 'locale_preferred']));
app.controller('ConceptMappingController', makeController('mappings', ['map_type', 'from_concept_url', 'to_concept_url']));

app.controller('ResourceExtraController', makeController('extras', ['extra_name', 'extra_value'], 'extra_name'));

// version's unique id is "id", not "uuid"
app.controller('SourceVersionController', makeController('versions', ['id', 'description', 'released'], 'id'));

app.controller('ConceptVersionController', function ($scope, $http, $location) {

        function loadItems() {
            var url = make_sub_url($location.absUrl(), 'versions/');
            set_debug($location, $scope);
            $http.get(url)
                .success(function (data) {
                    $scope.item_list = data;
                });
        } // loadItems

        loadItems();
    } // ConceptVersionController
);

app.controller('SourceSearchController', function ($scope, $http, $location) {

        function doSearch(search) {
            var url = $location.absUrl()
            url += '?q=' + search.text
            console.log(search.text);
            console.log(url);
            location = url
        }; // doSearch

        $scope.doSearch = doSearch

        function loadItems() {

            var url = $location.absUrl() + 'versions/';
            $http.get(url)
                .success(function (data) {
                    $scope.item_list = data;
                    console.log('versions:');
                    console.log($scope.item_list);
                });
        } // loadItems

        //        loadItems();

    } // SourceSearchController
);


app.controller('ConceptController', function ($scope, $http, $location) {

        $scope.alerts = [];
        $scope.item = null;

        function addItem(item) {
            // Create new concept

            var data = angular.copy(item);

            // translate text to code for locale
            data['locale'] = locale_by_name($scope.locale_choices, item['locale']).code;

            var config = null;

            var url = $location.absUrl();
            console.log('posting:' + url);
            $http.post(url, data, null)
                .success(function (data, status, headers, config) {
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    //                $scope.item = null;
                    var u = $location.absUrl().replace(/create\//, '');
                    console.log('replace:' + u);
                    //                window.location = u;
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });
                });


        } // addItem()

        $scope.addItem = addItem;

        function startEdit() {
            var url = $location.absUrl();
            $http.get(url)
                .success(function (data, status, headers, config) {
                    console.log(data);
                    $scope.item = data;
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data.message);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });
                });
        };


        function updateItem(item) {

            var data = angular.copy(item);
            console.log('update item' + item);
            var config = null;

            var url = $location.absUrl();
            $http.post(url, data, null)
                .success(function (data, status, headers, config) {
                    console.log(data);
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    loadItems();
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data.message);
                    $scope.alerts.push({
                        type: 'danger',
                        msg: data.message
                    });
                });

            $scope.editedItem = null;
        } // updateItem

        $scope.updateItem = updateItem;

        function loadItems() {

            var url = '/core/options/concept_classes/';
            $http.get(url)
                .success(function (data) {
                    $scope.concept_classes = data;
                });

            url = '/core/options/locales/';
            $http.get(url)
                .success(function (data) {
                    $scope.locale_choices = data;
                });

            url = '/core/options/datatypes/';
            $http.get(url)
                .success(function (data) {
                    $scope.datatypes = data;
                });

        } // loadItems

        loadItems();
        if (endsWith($location.absUrl(), 'edit/')) {
            startEdit();
        }
        ;

    } // ConceptController
);


/*
 Controller to handle Mapping CRUD.

 */
app.controller('MappingController', function ($scope, $http, $location) {

    $scope.isCreatingItem = false;
    $scope.isEditingItem = false;
    $scope.editedItem = null;
    $scope.item = null;
    $scope.alerts = [];

    function resetCreateForm() {
        $scope.newItem = {};
    }

    function startCreatingItem() {
        $scope.isCreatingItem = true;
        $scope.isEditingItem = false;
        resetCreateForm();
    }

    function cancelCreatingItem() {
        $scope.isCreatingItem = false;
    }

    function startEditingItem() {
        $scope.isCreatingItem = false;
        $scope.isEditingItem = true;
    }

    function cancelEditingItem() {
        $scope.isEditingItem = false;
    }

    function shouldShowCreatingItem() {
        return !$scope.isEditingItem;
    }

    function shouldShowEditingItem() {
        return $scope.isEditingItem && !$scope.isCreatingItem;
    }

    function setEditedItem(item) {
        // Set the current edited object, copy otherwise Angular will update the real thing
        $scope.editedItem = angular.copy(item);
        $scope.editedItem.is_external = !item.to_concept_url;

        console.log("editing...");
        console.log($scope.editedItem);
    };

    $scope.startCreatingItem = startCreatingItem;
    $scope.cancelCreatingItem = cancelCreatingItem;
    $scope.startEditingItem = startEditingItem;
    $scope.cancelEditingItem = cancelEditingItem;
    $scope.shouldShowCreatingItem = shouldShowCreatingItem;
    $scope.shouldShowEditingItem = shouldShowEditingItem;
    $scope.setEditedItem = setEditedItem;

    function addItem(item) {

        var data = angular.copy(item);
        var config = null;
        console.log(data);
        data['from_concept_url'] = URI.parse($location.absUrl()).path;

        if (data.source_type == 'external') {
            delete data.to_concept_url;
        } else {
            delete data.to_source_url;
            delete data.to_concept_code;
            delete data.to_concept_name;
        }
        delete data.source_type;
        console.log(data);

        var url = make_sub_url($location.absUrl(), 'mappings/');
        $http.post(url, data, null)
            .success(function (data, status, headers, config) {
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                loadItems();
            })
            .error(function (data, status, headers, config) {
                $scope.alerts.push({
                    type: 'danger',
                    msg: data.message
                });
            });

        resetCreateForm();
        cancelCreatingItem();
    } // addItem()

    $scope.addItem = addItem;

    function updateItem(item) {

        var data = angular.copy(item);
        console.log('update item');
        console.log(item);
        var config = null;

        $http.post(item.url, data, null)
            .success(function (data, status, headers, config) {
                console.log(data);
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                loadItems();
            })
            .error(function (data, status, headers, config) {
                console.log('ERROR:' + data.message);
                $scope.alerts.push({
                    type: 'danger',
                    msg: data.message
                });
            });

        $scope.editedItem = null;
        cancelEditingItem();
    } // updateItem

    $scope.updateItem = updateItem;

    function deleteItem(item) {

        var config = null;

        var target = item.to_concept_url || item.to_concept_code;
        if (!confirm("Are you sure you want to delete mapping to " + target + "?")) {
            return;
        }

        console.log('deleting mapping:');
        console.log(item);
        $http.delete(item.url)
            .success(function (data, status, headers, config) {
                console.log(data);
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                loadItems();
            })
            .error(function (data, status, headers, config) {
                console.log('DEL error' + data);
                $scope.alerts.push({
                    type: 'danger',
                    msg: data.message
                });

            });
    } // deleteItem()

    $scope.deleteItem = deleteItem;

    function loadItems() {

        var url = '/core/options/map_types/';
        $http.get(url)
            .success(function (data) {
                $scope.map_types = data;
            });

        var concept_url = URI.parse($location.absUrl()).path;
        url = make_sub_url($location.absUrl(), 'mappings/');
        $http.get(url)
            .success(function (data) {

                // split data into separate list because we have
                // some special cases
                $scope.q_and_a_list = [];
                $scope.item_list = [];
                $scope.inv_item_list = [];
                $scope.inv_q_and_a_list = [];

                for (var i = 0; i < data.length; i++) {
                    var m = data[i];
                    if (m.map_type === 'Q-AND-A') {
                        if (m.to_concept_url === concept_url)
                            $scope.inv_q_and_a_list.push(m);
                        else $scope.q_and_a_list.push(m);
                    }
                    else {
                        $scope.item_list.push(m);
                    }
                }
            });


    }; // loadItems

    loadItems();
    if (endsWith($location.absUrl(), 'edit/')) {
        startEdit();
    }
    ;

}); // MappingController


// Simple function to handle removing member from org
function removeMember(orgId, memId) {
    alert(orgId);
    alert(memId);
};

app.controller('MemberRemoveController', function ($scope, $uibModal,
                                                   $location, $http, $log) {

    $scope.alerts = [];

    var doRemove = function (org, username) {
        var url = $location.absUrl() + 'members/remove/' +
            username + '/';
        $http.post(url)
            .success(function (data, status, headers, config) {
                // How do we push to the outer template's alert?
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                window.location = $location.absUrl();
            })
            .error(function (data, status, headers, config) {
                $log.info('error');
                $log.info(data);
                $scope.alerts.push({
                    type: 'error',
                    msg: data.message
                });
            });
    }; // doRemove


    $scope.removeMember = function (org, username) {
        $scope.org = org;
        $scope.username = username;
        var modalInstance = $uibModal.open({
            templateUrl: 'myModalContent.html',
            // controller: 'MemberRemoveModalController',
            size: 'sm',
            scope: $scope,
        });

        modalInstance.result.then(
            function () {
                doRemove(org, username);

            }, function () {
                // dismissed...
            });
    };
});

app.controller('AddReferencesController', function ($scope, $uibModal, Reference) {
    $scope.pageObj = {};
    $scope.ownerType = 'orgs';
    $scope.resourceContainerType = 'sources';
    $scope.pageObj.cascadeMappings = true;
    $scope.REFERENCE_LIMIT = 10;

    $scope.getOwners = function () {
        $scope.resourceContainers = [];
        $scope.concepts = null;
        $scope.mappings = null;
        Reference.getOwners($scope.ownerType)
            .success(function (result) {
                $scope.owners = result;
            })
            .error(function (error) {
                console.log(error);
            })
    };

    $scope.getResourceContainers = function () {
        if (!$scope.owner) {
            return;
        }
        $scope.resourceContainerVersions = [];
        $scope.resourceContainer = null;
        $scope.concepts = null;
        $scope.mappings = null;
        Reference.getResourceContainers($scope.ownerType, $scope.resourceContainerType, $scope.owner)
            .success(function (result) {
                $scope.resourceContainers = result;
            })
            .error(function (error) {
                console.log(error);
            });
    };

    $scope.getResourceContainerVersions = function () {
        if (!$scope.resourceContainer) {
            return;
        }
        Reference.getResourceContainerVersions($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer)
            .success(function (result) {
                $scope.resourceContainerVersions = result;
            })
            .error(function (error) {
                console.log(error);
            });
    };

    $scope.getResourceContainerConcepts = function (page) {
        if (!$scope.owner || !$scope.resourceContainer) {
            return;
        }

        $scope.loading = true;

        var params = {
            limit: $scope.REFERENCE_LIMIT,
            page: page,
            includeRetired: true,
            q: '*' + ($scope.pageObj.search || '') + '*'
        };
        Reference.getResourceContainerVersionConcepts($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer, $scope.resourceContainerVersion, params)
            .success(function (result) {
                $scope.concepts = result;
            })
            .error(function (error) {
                console.log(error);
            })
            .finally(function () {
                $scope.loading = false;
            });
    };

    $scope.formatResourceContainerVersion = function (resourceContainerVersion) {
        return resourceContainerVersion.id + (resourceContainerVersion.retired ? ' (Retired)' : (resourceContainerVersion.released ? ' (Released)' : ''));
    };


    $scope.getResourceContainerMappings = function (page) {
        if (!$scope.owner || !$scope.resourceContainer) {
            return;
        }
        $scope.loading = true;

        var params = {
            limit: $scope.REFERENCE_LIMIT,
            page: page,
            includeRetired: true,
            q: '*' + ($scope.pageObj.search || '') + '*'
        };
        Reference.getResourceContainerVersionMappings($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer, $scope.resourceContainerVersion, params)
            .success(function (result) {
                $scope.mappings = result;
            })
            .error(function (error) {
                console.log(error);
            })
            .finally(function () {
                $scope.loading = false;
            });
    };

    var _getResourceExpressions = function (resources) {
        return resources.items.filter(function (resource) {
            return resource.isSelected;
        }).map(function (resource) {
            return resource.version_url;
        });
    };

    var _getUri = function () {
        var ownerIdentifier = $scope.ownerType === 'orgs' ? $scope.owner.id : $scope.owner.username;
        var resourceIdentifier = $scope.resourceContainerType === 'sources' ? $scope.resourceContainer.name : $scope.resourceContainer.id;
        return '/' + $scope.ownerType + '/' + ownerIdentifier + '/' + $scope.resourceContainerType + '/' + resourceIdentifier + '/' + $scope.resourceContainerVersion.id + '/';
    };

    $scope.addMultipleReferences = function () {
        var payload = {
            uri: _getUri(),
            search_term: '*' + ($scope.pageObj.search || '') + '*',
            concepts: $scope.pageObj.selectAllConcepts ? '*' : _getResourceExpressions($scope.concepts),
            mappings: $scope.pageObj.selectAllMappings ? '*' : _getResourceExpressions($scope.mappings)
        };

        $scope.addReferences(payload, false);
    };

    $scope.addSingleReferences = function () {
        var payload = {
            expressions: [$scope.singleReference]
        };
        $scope.addReferences(payload, true);
    };

    $scope.multipleReferencesAddButtonClicked = function () {
        var selectedConceptCount = $scope.pageObj.selectAllConcepts ? $scope.concepts.items.length : _getResourceExpressions($scope.concepts).length;
        var selectedMappingCount = $scope.pageObj.selectAllMappings ? $scope.mappings.items.length : _getResourceExpressions($scope.mappings).length;
        $scope.pageObj.selectedReferenceCount = selectedConceptCount + selectedMappingCount;
        if (selectedConceptCount > 0) {
            $scope.openConfirmModal();
        } else {
            $scope.addMultipleReferences();
        }
    };

    $scope.openConfirmModal = function () {
        $scope.confirmModal = $uibModal.open({
            animation: true,
            templateUrl: 'confirm-modal.html',
            scope: $scope
        });
    };

    $scope.closeConfirmModal = function () {
        $scope.confirmModal.close();
    };

    $scope.confirmConfirmModal = function () {
        $scope.confirmModal.close();
        $scope.addMultipleReferences();
    };

    $scope.openErrorModal = function () {
        $scope.errorModal = $uibModal.open({
            animation: true,
            templateUrl: 'error-modal.html',
            scope: $scope
        });
    };

    $scope.closeErrorModal = function () {
        $scope.errorModal.close();
    };

    $scope.addReferences = function (payload, addingSingle) {
        $scope.addingSingle = addingSingle;
        var cascadeParameter = !addingSingle && $scope.pageObj.cascadeMappings ? 'sourcemappings' : 'none';
        Reference.addReferences(payload, cascadeParameter)
            .success(function (result) {
                if ($scope.pageObj.selectAllConcepts || $scope.pageObj.selectAllMappings) {
                    alertify.success(
                        'We have started adding all the references, it might take some time for all references to reflect. Try to refresh the references tab in some time.', 3
                    );
                    setTimeout(function () {
                        location.pathname = result.success_url;
                    }, 3000);
                    return;
                }

                $scope.added = result.update_results.filter(function (result) {
                    return result.added;
                });

                $scope.errors = result.errors || result.update_results.filter(function (result) {
                        return !result.added;
                    }).reduce(function (hash, curr) {
                        hash[curr.expression] = curr.message[0];
                        return hash
                    }, {});

                if (_.size($scope.errors))
                    $scope.openErrorModal();

                if (!_.size($scope.errors))
                    location.pathname = result.success_url;

            })
            .error(function (error) {
                console.log("Error when adding references: " + error);
                console.log(error)
            })
            .finally(function () {
                $scope.loading = false;
                $scope.pageObj.cascadeMappings = true;
            });
    };

})
;

app.factory('Reference', function ($http) {
    var Reference = this;
    var DEFAULT_PER_PAGE = 10;

    Reference.getOwners = function (ownerType) {
        return $http.get('/' + ownerType + '/');
    };

    Reference.getResourceContainers = function (ownerType, resourceContainerType, owner) {
        var id = ownerType === 'orgs' ? owner.id : owner.username;

        return $http.get('/' + ownerType + '/' + id + '/' + resourceContainerType + '/');
    };

    Reference.getResourceContainerVersions = function (ownerType, resourceContainerType, owner, resourceContainer) {
        var ownerIdentifier = ownerType === 'orgs' ? owner.id : owner.username;
        var resourceIdentifier = resourceContainerType === 'sources' ? resourceContainer.name : resourceContainer.id;

        return $http.get('/' + ownerType + '/' + ownerIdentifier + '/' + resourceContainerType + '/' + resourceIdentifier + '/versions/');
    };

    Reference.getResourceContainerVersionConcepts = function (ownerType, resourceContainerType, owner, resourceContainer, resourceContainerVersion, params) {
        params = params || {
                limit: DEFAULT_PER_PAGE
            };
        var ownerIdentifier = ownerType === 'orgs' ? owner.id : owner.username;
        var resourceIdentifier = resourceContainerType === 'sources' ? resourceContainer.name : resourceContainer.id;
        var resourceContainerVersionId = resourceContainerVersion ? resourceContainerVersion.id : 'HEAD';

        return $http.get('/' + ownerType + '/' + ownerIdentifier + '/' + resourceContainerType + '/' + resourceIdentifier + '/' + resourceContainerVersionId + '/concepts/', {params: params});
    };

    Reference.getResourceContainerVersionMappings = function (ownerType, resourceContainerType, owner, resourceContainer, resourceContainerVersion, params) {
        params = params || {
                limit: DEFAULT_PER_PAGE
            };
        var ownerIdentifier = ownerType === 'orgs' ? owner.id : owner.username;
        var resourceIdentifier = resourceContainerType === 'sources' ? resourceContainer.name : resourceContainer.id;
        var resourceContainerVersionId = resourceContainerVersion ? resourceContainerVersion.id : 'HEAD';

        return $http.get('/' + ownerType + '/' + ownerIdentifier + '/' + resourceContainerType + '/' + resourceIdentifier + '/' + resourceContainerVersionId + '/mappings/', {params: params});
    };

    Reference.addReferences = function (references, cascadeParameter) {
        return $http.post(location.href + '?cascade=' + cascadeParameter + '&warning=show', references);
    };

    return this;
});

// WORK IN PROGRESS. DO NOT USE
app.directive('textField', function () {
    return {
        restrict: 'E',
        scope: {
            required: '@required',
            name: '@name',
            label: '@label',
            bindTo: '=',
            placeholder: '@placeholder',
            maxlength: '@maxlength'
        },
        template: '<div class="form-group {{required ? \'required\':\'\' }} ">' +
        '<label class="control-label" for="id_{{ name }}">{{ label }}</label>' +
        '<input class="form-control" id="id_{{name}}" maxlength="{{maxlength}}" name="{{name}}" ' +
        'placeholder="{{ placeholder}}" title="" type="text" ' +
        'ng-model="bindTo" /></div>'
    };
});

app.controller('CustomAttributesController', ['$scope', function ($scope) {

    $scope.addRow = function () {
        var extra = {key: '', value: ''};
        $scope.extras.push(extra);
    }

    $scope.removeRow = function (index) {
        $scope.extras.splice(index, 1);
    }

}])
    .directive('customAttributes', function () {
        return {
            restrict: 'E',
            scope: {
                extras: "="
            },
            replace: true,
            controller: 'CustomAttributesController',
            template: '<div class="form-group">' +
            '<label class="control-label col-md-12">Custom Attributes </label>' +
            '<div class="col-md-12">' +
            '<input name="extras" id="extras" class="form-control" type="hidden" value="{{ extras }}">' +
            '<div class="form-group row" ng-repeat="extra in extras">' +

            '<div class="col-md-5">' +
            '<label style="padding-left: 0px" for="inputKey" class="col-md-6 control-label">Attribute Name</label>' +
            '<input class="form-control" type="text" ng-model="extra.key" ng-required="extra.value">' +
            '</div>' +
            '<div class="col-md-6">' +
            '<label style="padding-left: 0px" for="inputValue" class="col-md-6 control-label">Value</label>' +
            '<textarea class="form-control"  rows="3" ng-model="extra.value"></textarea>' +
            '</div>' +
            '<span class="glyphicon glyphicon-trash pull-right" ng-click="removeRow($index)"></span>' +
            '</div>' +
            '<div class="form-group row">' +
            '<a ng-click="addRow()" style="cursor: pointer;"> <span class="glyphicon glyphicon-plus"></span> Add Custom Attribute</a>' +
            '</div>' +
            '</div>' +

            '</div>'
        };
    });

app.directive('conceptNameSynonym', function () {
    return {
        restrict: 'E',
        replace: true,
        scope: {
            names: '=',
            types: '=',
            locales: '=',
            defaultLocale: '=',
        },
        template: '' +
        '<div class="form-group" ng-init="addName()">' +
        '<input name="names" class="form-control" type="hidden" value="{{ names }}">' +
        '<label class="control-label col-md-12">Names & Synonyms</label>' +
        '<div id="names-and-synonyms" class="form-group" ng-repeat="name in names">' +
        '<span id="id-delete-name" class="delete-name-button glyphicon glyphicon-trash pull-right" ng-click="removeName($index)"></span>' +

        '<div class="form-group required col-md-2">' +
        '<label class="control-label">Locale</label>' +
        '<input class="awesomplete name-locale form-control" ng-model="name.locale" list="locale-list"' +
        'required="required" title="Choose the locale for the initial name and description">' +
        '<datalist id="locale-list">' +
        '<option ng-repeat="l in locales" value="{{l.code}}">{{l.name}}</option>' +
        '</datalist>'+
        '</div>' +

        '<div class="form-group required col-md-3">' +
        '<label class="control-label">Type</label>' +
        '<input class="name-type form-control" required="required" ng-model="name.name_type" list="type-list">' +
        '<datalist id="type-list">' +
        '<option ng-repeat="t in types">{{t}}</option>' +
        '</datalist>'+
        '</div>' +

        '<div class="form-group required col-md-3">' +
        '<label class="control-label">Name</label>' +
        '<input class="name-content form-control" ng-model="name.name"' +
        'placeholder="e.g. Tuberculosis of lung, confirmed by sputum microscopy with or without culture" required="required" title="" type="text">' +
        '</div>' +

        '<div class="form-group col-md-2">' +
        '<label class="control-label">External ID</label>' +
        '<input class="name-external-id form-control" ng-model="name.external_id" placeholder="External ID" type="text">' +
        '</div>' +

        '<div class="form-group col-md-2">' +
        '<label class="control-label"></label>' +
        '<div class="checkbox">' +
        '<label>' +
        '<input class="name-locale-preferred" checked="checked" type="checkbox" ng-model="name.locale_preferred">' +
        'Locale Preferred' +
        '</label>' +
        '</div>' +
        '</div>' +

        '</div>' +

        '<div class="form-group col-md-12">' +
        '<a class="add-name" ng-click="addName()" id="add-name-synonym" style="cursor: pointer;"> <span class="glyphicon glyphicon-plus"></span> Add name/synonym</a>' +
        '</div>' +

        '</div>',
        controller: function ($scope) {
            $scope.removeName = function (index) {
                $scope.names.splice(index, 1);
            };

            $scope.addName = function () {
                $scope.names = $scope.names || [];
                $scope.names.push({
                    'name': '',
                    'locale': $scope.defaultLocale,
                    'locale_preferred': false,
                    'name_type': 'Fully Specified'
                });
            };
        }
    };
});

app.directive('conceptDescription', function () {
    return {
        restrict: 'E',
        scope: {
            descriptions: "=",
            types: '=',
            locales: '=',
            defaultLocale: '=',
        },
        replace: true,
        template: '' +
        '<div class="form-group" ng-init="addDescription()">' +
        '<input name="descriptions" class="form-control" type="hidden" value="{{ descriptions }}">' +
        '<label class="control-label col-md-12">Description</label>' +
        '<div id="descriptions" class="form-group" ng-repeat="description in descriptions">' +
        '<span id="id-delete-description" class="delete-description-button glyphicon glyphicon-trash pull-right" ng-click="removeDescription($index)"></span>' +

        '<div class="form-group required col-md-2">' +
        '<label class="control-label">Locale</label>' +
        '<input class="name-locale form-control" ng-model="description.locale" list="locale-list"' +
        'required="required" title="Choose the locale for the initial name and description">' +
        '<datalist id="locale-list">' +
        '<option ng-repeat="l in locales" value="{{l.code}}">{{l.name}}</option>' +
        '</datalist>'+
        '</div>' +

        '<div class="form-group required col-md-3">' +
        '<label class="control-label">Type</label>' +
        '<input class="name-type form-control" required="required" ng-model="description.description_type" list="type-list">' +
        '<datalist id="type-list">' +
        '<option ng-repeat="t in types">{{t}}</option>' +
        '</datalist>'+
        '</div>' +

        '<div class="form-group col-md-3">' +
        '<label class="control-label">Description</label>' +
        '<textarea class="form-control" ng-model="description.description"' +
        'placeholder="e.g. Tuberculosis of lung, confirmed by sputum microscopy with or without culture"></textarea>' +
        '</div>' +

        '<div class="form-group col-md-2">' +
        '<label class="control-label">External ID</label>' +
        '<input class="form-control" ng-model="description.external_id" placeholder="Exernal ID" type="text">' +
        '</div>' +

        '<div class="form-group col-md-2">' +
        '<label class="control-label"></label>' +
        '<div class="checkbox">' +
        '<label>' +
        '<input checked="checked" type="checkbox" ng-model="description.locale_preferred">' +
        'Locale Preferred' +
        '</label>' +
        '</div>' +
        '</div>' +
        '</div>' +

        '<div class="form-group col-md-12">' +
        '<a ng-click="addDescription()" style="cursor: pointer;"> <span class="glyphicon glyphicon-plus"></span> Add Description</a>' +
        '</div>' +

        '</div>',
        controller: function ($scope) {
            $scope.removeDescription = function (index) {
                $scope.descriptions.splice(index, 1);
            };

            $scope.addDescription = function () {
                $scope.descriptions = $scope.descriptions || [];
                $scope.descriptions.push({
                    'description': '',
                    'locale': $scope.defaultLocale,
                    'locale_preferred': false,
                    'description_type': 'None'
                });
            };
        }
    };
});

$('div.release_unrelease_section #id_release').on('click', function (el) {
    var $el = $(el.toElement),
        version = $el.val(),
        released = $el.prop('checked'),
        url = ' /' + window.location.pathname.split('/').slice(1, 5).join('/') + '/' + version + '/json/edit/';
    $.ajax({
        type: "PUT",
        url: url,
        headers: {
            'X-CSRFToken': $.cookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        data: JSON.stringify({released: released}),
        dataType: 'json',
        contentType: 'application/json'
    }).done(function (data) {
        if (released) {
            $el.parents('li').find('.release-label-container .release-label').removeClass('hide');
            alertify.success('Successfully Released.', 3);
        } else {
            alertify.success('Successfully Un-Released.', 3);
            $el.parents('li').find('.release-label-container .release-label').addClass('hide');
        }
    }).fail(function (err) {
        alertify.error('Something unexpected happened!', 3);
        console.log(err)
    });
});

$('div.release_unrelease_section .resource_retire').on('click', function (ev) {
    var retireCheckboxElem = $(ev.toElement);
    var releaseCheckboxElem = retireCheckboxElem.siblings('#id_release');
    var retireLable = retireCheckboxElem.parents('li')
        .find('.release-label-container .retire-label');
    var releaseLabel = releaseCheckboxElem.parents('li')
        .find('.release-label-container .release-label');
    var breadCrumbLabel = retireCheckboxElem.closest('.list-group-item').find('.resource-label-id-code');
    var retired = retireCheckboxElem.prop('checked');
    var version = retireCheckboxElem.val();

    var url = ' /' + window.location.pathname.split('/').slice(1, 5).join('/') + '/' + version + '/json/edit/';
    $.ajax({
        type: "PUT",
        url: url,
        headers: {
            'X-CSRFToken': $.cookie('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        data: JSON.stringify({retired: retired}),
        dataType: 'json',
        contentType: 'application/json'
    }).done(function (data) {
        releaseCheckboxElem.prop({disabled: data.retired});
        if (data.retired) {
            setTimeout(function () {
                releaseLabel.addClass('hide')
            }, 0); // 0 timeout to tell the browser to execute it in the end.
            retireLable.removeClass('hide');
            breadCrumbLabel.addClass('strikethrough');
            alertify.success('Successfully Retired.', 3);
        } else {
            retireLable.addClass('hide');
            breadCrumbLabel.removeClass('strikethrough');
            alertify.success('Successfully Un-Retired.', 3);
        }

        if (data.released) {
            releaseLabel.removeClass('hide');
        } else {
            releaseLabel.addClass('hide');
        }
    }).fail(function () {
        alertify.error('Something unexpected happened!', 3);
    });
});

$('button.collection_version_delete').on('click', function (ev) {
    var button = $(ev.toElement);
    var version = button.data('id');

    var url = ' /' + window.location.pathname.split('/').slice(1, 5).join('/') + '/' + version + '/delete/';
    alertify.confirm(
        'Delete Version',
        'Are you sure you want to permanently delete this collection version <b>' + version + '</b>? This action cannot be undone! This will delete the version and its references. ' +
        'Concepts and mappings that are referenced in this collection version will not be affected.',
        function () {
            $.ajax({
                type: "DELETE",
                url: url,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                dataType: 'json',
                contentType: 'application/json'
            }).done(function (data) {
                button.closest('.list-group-item').remove();
                alertify.success('Successfully removed collection version.', 3);
            }).fail(function () {
                alertify.error('Something unexpected happened!', 3);
            });
        }, function () {
        }
    );
});

$('button.source_version_delete').on('click', function (ev) {
    var button = $(ev.toElement);
    var version = button.data('id');

    var url = ' /' + window.location.pathname.split('/').slice(1, 5).join('/') + '/' + version + '/delete/';
    alertify.confirm(
        'Delete Version',
        'Are you sure you want to permanently delete this source version <b>' + version + '</b>? This action cannot be undone! This will delete the version and all of its details. ' +
        'Concepts and mappings in this source version will not be affected.',
        function () {
            $.ajax({
                type: "DELETE",
                url: url,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                dataType: 'json',
                contentType: 'application/json'
            }).done(function (data) {
                button.closest('.list-group-item').remove();
                alertify.success('Successfully removed source version.', 3);
            }).fail(function () {
                alertify.error('Something unexpected happened!', 3);
            });
        }, function () {
        }
    );
});

if ($('#new_concept_base_url').length > 0) {
    var urlParts = _.compact(window.location.pathname.split('/')),

        conceptIdPlaceholder = '[concept-id]',

        titleFor = function (reference) {
            return 'Your new concept will live at: ' + reference;
        },

        updateHelpText = function () {
            var conceptId = $('#id_concept_id').val(),
                conceptIdText = conceptId || conceptIdPlaceholder;
            $('#new_concept_base_url').text(conceptReference);
            $('#new_concept_id').text(conceptIdText);
            $('#id_concept_id').attr('title', titleFor(conceptReference + conceptIdText));
        };

    urlParts.pop();

    var conceptReference = window.location.origin + "/" + urlParts.join('/') + "/";

    updateHelpText();

    $('#id_concept_id').keyup(function () {
        updateHelpText();
    });
}

var fireDownload = function (url) {
    alertify.success('Preparing CSV...');
    $.ajax({
        type: 'GET',
        url: url,
        dataType: "json",
        success: function (json) {
            if (json && json.url) {
                window.location.href = json.url;
                $('.alertify-notifier.ajs-top.ajs-right').children().click();
            } else {
                alertify.error('Something unexpected happened!', 3);
            }

        },
        error: function (err) {
            alertify.error('Something unexpected happened!', 3);
            console.dir(err);
        }
    });
};

//Stackoverflow - Anshu
$.urlParam = function (name) {
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(window.location.href);
    return results[1] || 0;
};

var httpURL = function (url) {
    if (_.includes(window.location.protocol, 'https:'))
        url = '//api.' + window.location.hostname.replace('www.', '');
    return url;
}

if ($('.download-csv').length > 0) {
    $('a.download-csv').on('click', function (el) {
        var downloadCaller = $('input#download-origin').val(),
            selectedTab = $('div.list-group a.active').text(),
            user = $("meta[name='user']").attr('content'),
            portInfo = ':8000',
            exactMatch = $("input[name='exact_match']:checked").size() > 0,
            url = '//' + window.location.hostname + portInfo;
        url = httpURL(url);

        getQueryParams = function (extraParams) {
            extraParams = extraParams || '';
            var mandatoryParams = "csv=true&user=" + user + extraParams,
                paramsWithExistingSearchParams = window.location.search + "&" + mandatoryParams;

            return _.isEmpty(window.location.search) ? "?" + mandatoryParams : paramsWithExistingSearchParams;
        },

            getSearchEntity = function () {
                var entity = _.find(['concepts', 'collections', 'mappings', 'sources', 'org', 'users'], function (type) {
                    return selectedTab.match(new RegExp(type, "i"))
                });
                if (entity == 'org') entity = 'orgs';

                return entity;
            },

            getURL = function () {
                var exactMatchParam = exactMatch ? '&exact_match=on' : '';
                if (downloadCaller) {
                    var entity = getSearchEntity();

                    return url + '/' + entity + '/' + getQueryParams("&type=" + entity + exactMatchParam);
                } else {
                    return url + window.location.pathname + getQueryParams("&type=repoSearch" + exactMatchParam);
                }
            };

        fireDownload(getURL());
    });
}
;

$('form#source_create_form .delete-source').on('click', function (ev) {
    var button = $(ev.toElement);
    alertify.confirm(
        'Delete Source',
        'Are you sure you want to permanently delete this source? This action cannot be undone! This will delete the entire source and all of its associated versions, concepts and mappings.',
        function () {
            $('form#source_create_form').submit();
        }, function () {
        }
    ).set('labels', {ok: 'Yes', cancel: 'No'});
});

$('form#collection_delete_form .delete-collection').on('click', function (ev) {
    var button = $(ev.toElement);
    alertify.confirm(
        'Delete Collection',
        'Are you sure you want to permanently delete this collection? This action cannot be undone! This will delete the entire collection and all of its associated versions and references. ' +
        'Concepts and mappings that are referenced in this collection will not be affected.',
        function () {
            $('form#collection_delete_form').submit();
        }, function () {
        }
    ).set('labels', {ok: 'Yes', cancel: 'No'});
});

$('#sourceVersion').change(function () {
    var versionInformation = $('#sourceVersion').find('option:selected').text();
    if (versionInformation === 'HEAD') {
        const IF_SELECTED_HEAD_VERSION_OF_SOURCE = 'When HEAD version selected, the latest version of concepts and mappings are listed';
        alertify.warning(IF_SELECTED_HEAD_VERSION_OF_SOURCE, 200)
    }
});

$('#collection_add_reference_form > div > input').keypress(function (e) {
    if (e.which == 13) {
        e.preventDefault();
    }
});

var triggerDownload = function (el) {
    var $el = $(el),
        user = $("meta[name='user']").attr('content');
    if (_.includes(window.location.protocol, 'https:'))
        url = '//api.' + window.location.hostname.replace('www.', '') + $el.data('uri') + '&user=' + user;
    else
        url = '//' + window.location.hostname + ':8000' + $el.data('uri') + '&user=' + user;
    fireDownload(url);
};
