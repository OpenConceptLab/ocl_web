/* Project specific Javascript goes here. */
var app = angular.module('ConceptApp', []);

app.controller('ConceptDescriptionController', function($scope, $http, $location) {
  $scope.message = 'Add description';

  function loadDescription() {

    var url = $location.absUrl() + 'descriptions/'
    $http.get(url)
        .success(function(data) {
          $scope.description_list = data;
          console.log($scope.description_list)
        })


  } // loadDescription

  function addDescription(desc) {

    var data = {
      description: desc.description,
      description_type: desc.descriptionType,
      locale: desc.locale,
      preferred_locale: desc.preferredLocale
    }

    var config = {
      params: {
        description: desc.description,
        description_type: desc.descriptionType,
        locale: desc.locale,
        preferred_locale: desc.preferredLocale
      }
    };

    $http.post($scope.formUrl, data, null)
      .success(function(data, status, headers, config)
      {
        console.log(data);
        $scope.message = data['message'];
        loadDescription();
      })
      .error(function(data, status, headers, config)
      {
        $scope.message = data['message'];
      });

  } // addDescription()



  $scope.addDescription = addDescription;


  function deleteDescription(desc) {

    var data = {
      description: desc.description,
      description_type: desc.descriptionType,
      locale: desc.locale,
      preferred_locale: desc.preferredLocale
    }

    var config = {
      params: {
        description: desc.description,
        description_type: desc.descriptionType,
        locale: desc.locale,
        preferred_locale: desc.preferredLocale
      }
    };

    if (confirm("Are you sure?")) {
 ;
    }
 
    return

    $http.post($scope.formUrl, data, null)
      .success(function(data, status, headers, config)
      {
        console.log(data);
        $scope.message = data['message'];
        loadDescription();
      })
      .error(function(data, status, headers, config)
      {
        $scope.message = data['message'];
      });

  } // deleteDescription()

  $scope.deleteDescription = deleteDescription;

  loadDescription();
});


app.controller('DescriptionAddController', function($scope, $http) {
  $scope.message = 'Add description';

  function addDescription(desc) {

    var data = {
      description: desc.description,
      description_type: desc.descriptionType,
      locale: desc.locale,
      preferred_locale: desc.preferredLocale
    }

    var config = {
      params: {
        description: desc.description,
        description_type: desc.descriptionType,
        locale: desc.locale,
        preferred_locale: desc.preferredLocale
      }
    };

    $http.post($scope.formUrl, data, null)
      .success(function(data, status, headers, config)
      {
        console.log(data);
        $scope.message = data['message'];
      })
      .error(function(data, status, headers, config)
      {
        $scope.message = data['message'];
      });

  } // addDescription()

  $scope.addDescription = addDescription;
});

app.controller('DescriptionListController', function($scope, $http, $location) {

  function loadDescription() {

    var url = $location.absUrl() + 'descriptions/'
    $http.get(url)
        .success(function(data) {
          $scope.description_list = data;
          console.log($scope.description_list)
        })


  } // loadDescription

  loadDescription();
})

