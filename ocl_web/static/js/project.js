/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', []);

// Make a controller that accesses the backend using a_url_part as the item type
function makeController(a_url_part, a_field_names) {

    return function conceptItemController($scope, $http, $location) {

        var url_part = a_url_part;  // from makeController
        var field_names = a_field_names;

        console.log('my url part:', url_part)
        $scope.message = '';
        $scope.isCreatingItem = false;
        $scope.isEditingItem = false;
        $scope.editedItem = null;
        $scope.item = null;

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
        }

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
                console.log($scope.item_list);
                });
        } // loadItems

      function addItem(item) {

        var data = {};
        for (var i=0; i < field_names.length; i++) {
            fn = field_names[i];
            data[fn] = item[fn];
        }

        var config = null;

        var url = $location.absUrl() + url_part + '/';
        $http.post(url, data, null)
          .success(function (data, status, headers, config) {
            $scope.message = data['message'];
            loadItems();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
          });

          resetCreateForm();
          cancelCreatingItem();
      } // addItem()



      $scope.addItem = addItem;

      function updateItem(item) {

        var data = {};
        for (var i=0; i < field_names.length; i++) {
            fn = field_names[i];
            data[fn] = item[fn];
        }

        var config = null;

        var url = $location.absUrl() + url_part + '/' + item.uuid + '/';
        $http.post(url, data, null)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.message = data['message'];
            loadItems();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
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

        var url = $location.absUrl() + url_part + '/' + item.uuid + '/';
        $http.delete(url)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.message = data['message'];
            loadItems();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
          });
      } // deleteItem()

      $scope.deleteItem = deleteItem;

      loadItems();

    } // conceptItemController

    } // makeController


// app.controller('ConceptDescriptionController', conceptItemController);
app.controller('ConceptDescriptionController', makeController('descriptions', ['description', 'description_type', 'locale', 'locale_preferred']));
app.controller('ConceptNameController', makeController('names', ['name', 'name_type', 'locale', 'locale_preferred']));
