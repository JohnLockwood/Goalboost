// create the module and name it alguitoApp
var alguitoApp = angular.module('alguitoApp', ['ngRoute']);

/*
alguitoApp.config(['$interpolateProvider', function($interpolateProvider) {
    $interpolateProvider.startSymbol('[[');
    $interpolateProvider.endSymbol(']]');
}]);
*/

// configure our routes
alguitoApp.config(function($routeProvider) {
    $routeProvider

        // route for the home page
        .when('/home', {
            templateUrl : 'home.html',
        })

        .when('/register', {
            templateUrl : 'register.html'

        });
});

// create the controller and inject Angular's $scope
alguitoApp.controller('mainController', function($scope) {
    // create a message to display in our view
    $scope.message = 'Everyone come and see how good I look!';
});