/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', ['ui.bootstrap']);

/* Add CSRF token for the web site. Note that we are setting the common defaults
   instead of post, because we need it for delete as well?
*/
app.config(function($httpProvider) {
    $httpProvider.defaults.headers.common['X-CSRFToken'] = $('input[name=csrfmiddlewaretoken]').val();
});


function locale_by_name(locale_choices, n) {
    for (var i=0; i<locale_choices.length; i++) {
        if (locale_choices[i].name == n) {
            return locale_choices[i];
        }
    }
};

function locale_by_code(locale_choices, c) {
    for (var i=0; i<locale_choices.length; i++) {
        if (locale_choices[i].code == c) {
            return locale_choices[i];
        }
    }
};

/* Make a controller that accesses the backend using a_url_part as the item type

   :param a_item_key: specifies the field name in the item object used to uniquely
   identify the object to the backend.
*/
function makeController(a_url_part, a_field_names, a_item_key) {

    return function conceptItemController($scope, $http, $location) {

        var url_part = a_url_part;  // from makeController
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
            for (var i=0; i<field_names.length; i++) {
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

            var url = $location.absUrl() + url_part + '/';
            $http.get(url)
                .success(function (data) {
                $scope.item_list = data;
                });
        } // loadItems

        function loadLocales() {

            var url = $location.protocol() + '://' + $location.host() + ':' + $location.port() + '/core/locales/';
            $http.get(url)
                .success(function (data) {
                $scope.locale_choices = data;
                });
        } // loadLocales

        function addItem(item) {

            // get form fields for API by name, specified
            // when controller is created.
            var data = {};
            for (var i=0; i < field_names.length; i++) {
                fn = field_names[i];
                // special case for locale, translate text to code for API
                if ('locale' == fn) {
                    data[fn] = locale_by_name($scope.locale_choices, item[fn]).code;
                }
                else {
                    data[fn] = item[fn];
                };
            }

            var config = null;

            var url = $location.absUrl() + url_part + '/';
            $http.post(url, data, null)
                .success(function (data, status, headers, config) {
                    $scope.alerts.push({type: 'success', msg: data.message});
                    loadItems();
                })
                .error(function (data, status, headers, config) {
                    console.log('ERROR:' + data);
                    $scope.alerts.push({type: 'danger', msg: data.message});
                });

            resetCreateForm();
            cancelCreatingItem();
        } // addItem()

        $scope.addItem = addItem;

        function updateItem(item) {

            var data = {};
            for (var i=0; i < field_names.length; i++) {
                fn = field_names[i];
                // special case for locale, translate text to code for API
                if ('locale' == fn) {
                    data[fn] = locale_by_name($scope.locale_choices, item[fn]).code;
                }
                else {
                    data[fn] = item[fn];
                };
            };

            var config = null;

            var url = $location.absUrl() + url_part + '/' + item[item_key] + '/';
            $http.post(url, data, null)
              .success(function (data, status, headers, config) {
                console.log(data);
                $scope.alerts.push({type: 'success', msg: data.message});
                loadItems();
              })
              .error(function (data, status, headers, config) {
                console.log('ERROR:' + data.message);
                $scope.alerts.push({type: 'danger', msg: data.message});
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
        console.log('DEL:' + item );
        var url = $location.absUrl() + url_part + '/' + item[item_key] + '/';
        $http.delete(url)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.alerts.push({type: 'success', msg: data.message});
            loadItems();
          })
          .error(function (data, status, headers, config) {
            console.log('DEL error' + data);
            $scope.alerts.push({type: 'danger', msg: data.message});

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
app.controller('ConceptDescriptionController', makeController('descriptions', ['description', 'description_type', 'locale', 'locale_preferred']));
app.controller('ConceptNameController', makeController('names', ['name', 'name_type', 'locale', 'locale_preferred']));

app.controller('ResourceExtraController', makeController('extras', ['extra_name', 'extra_value'], 'extra_name'));

// version's unique id is "id", not "uuid"
app.controller('SourceVersionController', makeController('versions', ['id', 'description', 'released'], 'id'));

app.controller('ConceptVersionController', function($scope, $http, $location) {

        function loadItems() {

            var url = $location.absUrl() + 'versions/';
            $http.get(url)
                .success(function (data) {
                $scope.item_list = data;
                });
        } // loadItems

        loadItems();
}// ConceptVersionController
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
                .success(function (data) {
                $scope.item_list = data;
                console.log('versions:');
                console.log($scope.item_list);
                });
        } // loadItems

//        loadItems();

}// SourceSearchController
)

