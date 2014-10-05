/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', []);

// Make a controller that accesses the backend using a_url_part as the item type
function makeController(a_url_part) {

    return function conceptItemController($scope, $http, $location) {

        var url_part = a_url_part;  // from makeController

        console.log('my url part:', url_part)
        $scope.message = '';
        $scope.isCreatingDescription = false;
        $scope.isEditingDescription = false;
        $scope.editedDescription = null;

        function startCreatingDescription() {
            $scope.isCreatingDescription = true;
            $scope.isEditingDescription = false;
        }

        function cancelCreatingDescription() {
            $scope.isCreatingDescription = false;
        }

        function startEditingDescription() {
            $scope.isCreatingDescription = false;
            $scope.isEditingDescription = true;
        }

        function cancelEditingDescription() {
            $scope.isEditingDescription = false;
        }

        function shouldShowCreatingDescription() {
            return !$scope.isEditingDescription;
        }

        function shouldShowEditingDescription() {
            return $scope.isEditingDescription && !$scope.isCreatingDescription;
        }

        function setEditedDescription(desc) {
            // Set the current edited object, copy otherwise Angular will update the real thing
            $scope.editedDescription = angular.copy(desc);
        }

        $scope.startCreatingDescription = startCreatingDescription;
        $scope.cancelCreatingDescription = cancelCreatingDescription;
        $scope.startEditingDescription = startEditingDescription;
        $scope.cancelEditingDescription = cancelEditingDescription;
        $scope.shouldShowCreatingDescription = shouldShowCreatingDescription;
        $scope.shouldShowEditingDescription = shouldShowEditingDescription;
        $scope.setEditedDescription = setEditedDescription;

        function loadDescription() {

            var url = $location.absUrl() + url_part + '/';
            $http.get(url)
                .success(function (data) {
                $scope.description_list = data;
                console.log($scope.description_list);
                });
        } // loadDescription

      function addDescription(desc) {

        var data = {
          description: desc.description,
          description_type: desc.description_type,
          locale: desc.locale,
          locale_preferred: desc.locale_preferred
        };

        var config = null;
        console.log(data);

        var url = $location.absUrl() + 'descriptions/';
        $http.post(url, data, null)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.message = data['message'];
            loadDescription();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
          });

      } // addDescription()



      $scope.addDescription = addDescription;

      function updateDescription(desc) {

        var data = {
          description: desc.description,
          description_type: desc.description_type,
          locale: desc.locale,
          locale_preferred: desc.locale_preferred
        };
        var config = null;

    //    var url = $location.absUrl() + 'descriptions/' + desc.uuid + '/';
        var url = $location.absUrl() + url_part + '/' + desc.uuid + '/';
        $http.post(url, data, null)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.message = data['message'];
            loadDescription();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
          });

        $scope.editedDescription = null;
        cancelEditingDescription();
      } // updateDescription

      $scope.updateDescription = updateDescription;

      function deleteDescription(desc) {

        var data = {
          description: desc.description,
          description_type: desc.descriptionType,
          locale: desc.locale,
          preferred_locale: desc.preferredLocale
        };

        var config = null;

        if (!confirm("Are you sure?")) {
          return;
        }

        var url = $location.absUrl() + 'descriptions/' + desc.uuid + '/';
        $http.delete(url, data, null)
          .success(function (data, status, headers, config) {
            console.log(data);
            $scope.message = data['message'];
            loadDescription();
          })
          .error(function (data, status, headers, config) {
            $scope.message = data['message'];
          });
      } // deleteDescription()

      $scope.deleteDescription = deleteDescription;

      loadDescription();
      console.log('my url part:', url_part);

    } // conceptItemController

    } // makeController


// app.controller('ConceptDescriptionController', conceptItemController);
app.controller('ConceptDescriptionController', makeController('descriptions'));