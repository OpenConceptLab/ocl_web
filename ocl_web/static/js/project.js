/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', ['ui.bootstrap']);

/* Add CSRF token for the web site. Note that we are setting the common defaults
   instead of post, because we need it for delete as well?
*/
app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
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
                        };
                    };
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
                            .success(function(data) {
                                $scope.item_list = data;
                            });
                    } // loadItems

                function loadLocales() {

                        var url = $location.protocol() + '://' + $location.host() + ':' + $location.port() + '/core/options/locales/';
                        $http.get(url)
                            .success(function(data) {
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
                            };
                        }

                        var config = null;

                        var url = $location.absUrl() + url_part + '/';
                        $http.post(url, data, null)
                            .success(function(data, status, headers, config) {
                                $scope.alerts.push({
                                    type: 'success',
                                    msg: data.message
                                });
                                loadItems();
                            })
                            .error(function(data, status, headers, config) {
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
                            };
                        };
                        var config = null;

                        var url = $location.absUrl() + url_part + '/' + item[item_key] + '/';
                        $http.post(url, data, null)
                            .success(function(data, status, headers, config) {
                                $scope.alerts.push({
                                    type: 'success',
                                    msg: data.message
                                });
                                loadItems();
                            })
                            .error(function(data, status, headers, config) {
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
                            .success(function(data, status, headers, config) {
                                console.log(data);
                                $scope.alerts.push({
                                    type: 'success',
                                    msg: data.message
                                });
                                loadItems();
                            })
                            .error(function(data, status, headers, config) {
                                console.log('DEL error' + data);
                                $scope.alerts.push({
                                    type: 'danger',
                                    msg: data.message
                                });

                            });
                    } // deleteItem()

                $scope.deleteItem = deleteItem;

                $scope.closeAlert = function(index) {
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

app.controller('ConceptVersionController', function($scope, $http, $location) {

        function loadItems() {
                var url = make_sub_url($location.absUrl(), 'versions/');
                set_debug($location, $scope);
                $http.get(url)
                    .success(function(data) {
                        $scope.item_list = data;
                    });
            } // loadItems

        loadItems();
    } // ConceptVersionController
);

app.controller('SourceSearchController', function($scope, $http, $location) {

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
                    .success(function(data) {
                        $scope.item_list = data;
                        console.log('versions:');
                        console.log($scope.item_list);
                    });
            } // loadItems

        //        loadItems();

    } // SourceSearchController
);


app.controller('ConceptController', function($scope, $http, $location) {

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
                    .success(function(data, status, headers, config) {
                        $scope.alerts.push({
                            type: 'success',
                            msg: data.message
                        });
                        //                $scope.item = null;
                        var u = $location.absUrl().replace(/create\//, '');
                        console.log('replace:' + u);
                        //                window.location = u;
                    })
                    .error(function(data, status, headers, config) {
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
                .success(function(data, status, headers, config) {
                    console.log(data);
                    $scope.item = data;
                })
                .error(function(data, status, headers, config) {
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
                    .success(function(data, status, headers, config) {
                        console.log(data);
                        $scope.alerts.push({
                            type: 'success',
                            msg: data.message
                        });
                        loadItems();
                    })
                    .error(function(data, status, headers, config) {
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
                    .success(function(data) {
                        $scope.concept_classes = data;
                    });

                url = '/core/options/locales/';
                $http.get(url)
                    .success(function(data) {
                        $scope.locale_choices = data;
                    });

                url = '/core/options/datatypes/';
                $http.get(url)
                    .success(function(data) {
                        $scope.datatypes = data;
                    });

            } // loadItems

        loadItems();
        if (endsWith($location.absUrl(), 'edit/')) {
            startEdit();
        };

    } // ConceptController
);



/*
    Controller to handle Mapping CRUD.

*/
app.controller('MappingController', function($scope, $http, $location) {

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
        $scope.editedItem.is_external = ! item.to_concept_url;

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
            .success(function(data, status, headers, config) {
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                loadItems();
            })
            .error(function(data, status, headers, config) {
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
                .success(function(data, status, headers, config) {
                    console.log(data);
                    $scope.alerts.push({
                        type: 'success',
                        msg: data.message
                    });
                    loadItems();
                })
                .error(function(data, status, headers, config) {
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
            .success(function(data, status, headers, config) {
                console.log(data);
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                loadItems();
            })
            .error(function(data, status, headers, config) {
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
            .success(function(data) {
                $scope.map_types = data;
            });

        var concept_url = URI.parse($location.absUrl()).path;
        url = make_sub_url($location.absUrl(), 'mappings/');
        $http.get(url)
            .success(function(data) {

                // split data into separate list because we have
                // some special cases
                $scope.q_and_a_list = [];
                $scope.item_list = [];
                $scope.inv_item_list = [];
                $scope.inv_q_and_a_list = [];

                for (var i=0; i<data.length; i++) {
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
    };

}); // MappingController


// Simple function to handle removing member from org
function removeMember(orgId, memId) {
    alert(orgId);
    alert(memId);
};

app.controller('MemberRemoveController', function($scope, $uibModal,
                                                  $location, $http, $log) {

    $scope.alerts = [];

    var doRemove = function(org, username) {
        var url = $location.absUrl() + 'members/remove/' +
            username + '/';
        $http.post(url)
            .success(function(data, status, headers, config) {
                // How do we push to the outer template's alert?
                $scope.alerts.push({
                    type: 'success',
                    msg: data.message
                });
                window.location = $location.absUrl();
            })
            .error(function(data, status, headers, config) {
                $log.info('error');
                $log.info(data);
                $scope.alerts.push({
                    type: 'error',
                    msg: data.message
                });
            });
        }; // doRemove


    $scope.removeMember = function(org, username) {
        $scope.org = org;
        $scope.username = username;
        var modalInstance = $uibModal.open({
            templateUrl: 'myModalContent.html',
            // controller: 'MemberRemoveModalController',
            size: 'sm',
            scope: $scope,
        });

    modalInstance.result.then(
        function() {
            doRemove(org, username);

        }, function() {
            // dismissed...
        });
    };
});

app.controller('AddReferencesController', function($scope, Reference) {
    $scope.pageObj = {};
    $scope.ownerType = 'orgs';
    $scope.resourceContainerType = 'sources';
    $scope.REFERENCE_LIMIT = 10;

    $scope.getOwners = function() {
        $scope.resourceContainers = [];
        Reference.getOwners($scope.ownerType)
            .success(function(result) {
                $scope.owners = result;
            })
            .error(function(error) {
                window.alert(error);
            })
    };

    $scope.getResourceContainers = function() {
        if(!$scope.owner) {
            return;
        }
        $scope.resourceContainerVersions = [];
        $scope.resourceContainer = null;
        Reference.getResourceContainers($scope.ownerType, $scope.resourceContainerType, $scope.owner)
            .success(function(result) {
                $scope.resourceContainers = result;
            })
            .error(function(error) {
                window.alert(error);
            });
    };

     $scope.getResourceContainerVersions = function() {
        if(!$scope.resourceContainer) {
            return;
        }
        Reference.getResourceContainerVersions($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer)
            .success(function(result) {
                $scope.resourceContainerVersions = result;
            })
            .error(function(error) {
                window.alert(error);
            });
    };

    $scope.getResourceContainerConcepts = function(page) {
        if(!$scope.owner || !$scope.resourceContainer) {
            return;
        }
        $scope.loading = true;

        var params = {limit: $scope.REFERENCE_LIMIT, page: page};
        Reference.getResourceContainerVersionConcepts($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer, $scope.resourceContainerVersion, params)
            .success(function(result) {
                $scope.concepts = result;
            })
            .error(function(error) {
                window.alert(error);
            })
            .finally(function() {
                $scope.loading = false;
            });
    };

    $scope.getResourceContainerMappings = function(page) {
        if(!$scope.owner || !$scope.resourceContainer) {
            return;
        }
        $scope.loading = true;

        var params = {limit: $scope.REFERENCE_LIMIT, page: page};

        Reference.getResourceContainerVersionMappings($scope.ownerType, $scope.resourceContainerType, $scope.owner, $scope.resourceContainer, $scope.resourceContainerVersion, params)
            .success(function(result) {
                $scope.mappings = result;
            })
            .error(function(error) {
                window.alert(error);
            })
            .finally(function() {
                $scope.loading = false;
            });
    };

    $scope.addMultipleReferences = function() {
      references = [];

      references = references.concat(
        $scope.concepts.items.filter(function(concept) { return concept.isSelected; })
      ).concat(
        $scope.mappings.items.filter(function(mapping) { return mapping.isSelected; })
      ).map(function(reference) { return reference.url });

      $scope.addReferences(references);
    };

    $scope.addReferences = function(references) {
        Reference.addReferences(references)
            .success(function(result) {
              if(!_.size(result.errors)) {
                location.pathname = result.success_url;
                return;
              }
              window.alert(JSON.stringify(result.errors));
            })
            .error(function(error) {
                window.alert(error);
            })
            .finally(function() {
                $scope.loading = false;
            });
    };

    $scope.selectAllReferencesChanged = function(allReferences, selectAllModel) {
      angular.forEach(allReferences, function(reference) {
        reference.isSelected = selectAllModel;
      });
    };

    $scope.referenceSelectionChanged = function(reference, allReferences) {
      if(!reference.isSelected) {
        return false;
      }
      var selectedReferences = allReferences.filter(function(ref) {
        return ref.isSelected;
      });
      if(selectedReferences.length === allReferences.length) {
        return true;
      }
    };

});

app.factory('Reference', function($http) {
    var Reference = this;
    var DEFAULT_PER_PAGE = 10;

    Reference.getOwners = function(ownerType) {
        return $http.get('/' + ownerType + '/');
    };

    Reference.getResourceContainers = function(ownerType, resourceContainerType, owner) {
        var id = ownerType === 'orgs' ? owner.id : owner.username;
        return $http.get('/' + ownerType + '/' + id + '/' + resourceContainerType + '/');
    };

    Reference.getResourceContainerVersions = function(ownerType, resourceContainerType, owner, resourceContainer) {
        var id = ownerType === 'orgs' ? owner.id : owner.username;
        return $http.get('/' + ownerType + '/' + id + '/' + resourceContainerType + '/' + resourceContainer.name+ '/versions/');
    };

    Reference.getResourceContainerVersionConcepts = function(ownerType, resourceContainerType, owner, resourceContainer, resourceContainerVersion, params) {
        params = params || {
            limit: DEFAULT_PER_PAGE
        };
        var id = ownerType === 'orgs' ? owner.id : owner.username;
        var resourceContainerVersionId = resourceContainerVersion ? resourceContainerVersion.id : 'HEAD';

        return $http.get('/' + ownerType +'/' + id + '/' + resourceContainerType +'/' + resourceContainer.name + '/' + resourceContainerVersionId + '/concepts/', {params: params});
    };

    Reference.getResourceContainerVersionMappings = function(ownerType, resourceContainerType, owner, resourceContainer, resourceContainerVersion, params) {
        params = params || {
            limit: DEFAULT_PER_PAGE
        };
        var id = ownerType === 'orgs' ? owner.id : owner.username;
        var resourceContainerVersionId = resourceContainerVersion ? resourceContainerVersion.id : 'HEAD';

        return $http.get('/' + ownerType +'/' + id + '/' + resourceContainerType +'/' + resourceContainer.name + '/' + resourceContainerVersionId + '/mappings/', {params: params});
    };

    Reference.addReferences = function(references) {
        return $http.post(location.href, references);
    };

    return this;
});

// WORK IN PROGRESS. DO NOT USE
app.directive('textField', function() {
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

$('a.delete-reference').on('click', function () {
    var selectedReferences = $("input[name='reference']:checked"),

        references = _.map(selectedReferences, function (el) { return el.value; }),

        url = ' /' + window.location.pathname.split('/').slice(1,5).join('/') + '/references/delete/' + '?references=' + references,

        confirmSuccess = function () {
            $.ajax({
                type: "DELETE",
                url: url,
                headers: {
                    'X-CSRFToken': $.cookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                dataType: 'json'
            }).done(function () {
                _.each($(".references input[type=checkbox]:checked"), function (el) {
                    $(el).parent().parent().remove();
                });

                alertify.success('Successfully removed.', 3);
                $('.alert.alert-info').parent().remove();
            }).fail(function (err) {
                alertify.error('Something unexpected happened!', 3);
                console.log(err)
            });
        };
    if(_.size(references) > 0) {
        alertify.confirm('Delete Reference', 'Do you want to remove the selected Reference(s) and associated values from Concepts and Mappings tab?', confirmSuccess, function () {});
    } else {
        alertify.warning('Please select references!')
    }
});

$('div.release_unrelease_section #id_release').on('click', function (el) {
    var $el = $(el.toElement),
        version = $el.val(),
        released = $el.prop('checked'),
        url = ' /' + window.location.pathname.split('/').slice(1,5).join('/') + '/'+version+'/json/edit/';
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
            var dom = "<span class='label label-primary release-label'>Released</span>";
            $el.parents('li').find('.release-label-container').append(dom);
            alertify.success('Successfully Released.', 3);
        } else {
            alertify.success('Successfully Un-Released.', 3);
            $el.parents('li').find('.release-label-container .release-label').remove();
        }
    }).fail(function (err) {
        alertify.error('Something unexpected happened!', 3);
        console.log(err)
    });


});
