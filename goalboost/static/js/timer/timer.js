/*
function TimeFormatter() {
    // Formatting functions:
    this.formatSeconds = function(timeInSeconds) {
        var hours = 0;
        var minutes = 0;
        var seconds= timeInSeconds % 60;
        //var suffix = "seconds";
        var timeStr = this.pad(seconds, 2, 0);

        if (timeInSeconds >= 60) {
            minutes = Math.floor(timeInSeconds /60) % 60;
            timeStr = this.pad(minutes, 2, 0) + ":" + timeStr;
            // suffix = "minutes";
        }
        if (timeInSeconds >= 3600) {
            hours = Math.floor(timeInSeconds / 3600);
            timeStr = hours + ":" + timeStr;
            //  suffix = "hours";
        }

        return timeStr; // + " " + suffix;
    };

    // Left-zero padding for minutes, seconds, etc.
    this.pad = function(n, width, z) {
        z = z || '0';
        n = n + '';
        return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
    };
}
*/
var myApp = angular.module('myApp', []);

myApp.controller('TimerController', ['$scope',  '$http', function($scope, $http) {
    //$scope.someTimerValue = 99;
    //$scope.timeFormatter = new TimeFormatter();
    $scope.timeFormatted = "0:00:00" ; // $scope.timeFormatter.formatSeconds(1);

    $scope.startButtonClass = "success";
    $scope.startButtonText = "Start";
    $scope.timers = [];
    $scope.timers_json = $scope.timers;
    $scope.startDisplayed = true;

    $scope.startTimer = function()  {
        console.log("startTimer");
        $scope.startButtonClass = "alert";
        $scope.startButtonText = "Stop";
        $scope.timers.push({"startTime": new Date()})

        $scope.updateTimersJson();

    }
    $scope.stopTimer = function()  {

        console.log("stopTimer");
        $scope.startButtonText = "Start";
        $scope.startButtonClass = "success";
        if ($scope.timers.length == 0)
            return;

        $scope.timers[$scope.timers.length - 1]["endTime"] = new Date();
        $scope.updateTimersJson();
    }
    $scope.updateTimersJson = function() {
        $scope.timers_json = JSON.stringify($scope.timers, "\n", 2);
    }

    $scope.$watch('startDisplayed', function(){
        $scope.startDisplayed ?  $scope.stopTimer() : $scope.startTimer() ;
    });

}]);
