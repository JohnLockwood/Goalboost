function getScriptParams() {
    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length - 1];
    var scriptName = lastScript;
    return {
        userId: scriptName.getAttribute('data-userId'),
        authToken: scriptName.getAttribute('data-authToken'),
        userEmail: scriptName.getAttribute('data-userEmail')
    }
}

var timerApp = angular.module('timerApp', []);

// Save it here while in scope so can  be used by controller
scriptParams = getScriptParams();

angular.module('timerApp', ["ngSanitize"]).filter('checkEmpty',function($sce){
        return function(input){
            if(angular.isString(input) && !(angular.equals(input,null) || angular.equals(input,'')))
                return input;
            else
                return $sce.trustAsHtml('&nbsp;');
        };
    });


angular.module('timerApp').filter("formatTime", function() {
    return function (timeInSeconds) {
        // Left-zero padding for minutes, seconds, etc.
        var pad = function(n, width, z) {
            z = z || '0';
            n = n + '';
            return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
        };
        var hours = 0;
        var minutes = 0;
        var seconds= timeInSeconds % 60;
        //var suffix = "seconds";
        var timeStr = pad(seconds, 2, 0);
        if (timeInSeconds >= 60) {
            minutes = Math.floor(timeInSeconds /60) % 60;
            timeStr = pad(minutes, 2, 0) + ":" + timeStr;
        }
        else {
            timeStr = pad("00", 2, 0) + ":" + timeStr;
        }
        if (timeInSeconds >= 3600) {
            hours = Math.floor(timeInSeconds / 3600);
            timeStr = hours + ":" + timeStr;
        }

        return timeStr; // + " " + suffix;
    }
});

// angular.directive('timerApp')
angular.module('timerApp').directive('dateFormatter', function($log) {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, controller) {

            controller.$formatters.push(function(value) {
                $log.log(value);
                $log.debug(value);
                return value;
            });
            controller.$parsers.push(function(value) {
                $log.log(value);
                return value;
            });
        }
    };
});

/* Directives */

angular.module('timerApp').directive('datePicker',
    function DatePicker(){
        return {
            require: 'ngModel',
            restrict: 'A',
            scope: { format: "=" },
            link: function(scope, element, attrs, ngModel){
                if(typeof(scope.format) == "undefined"){ scope.format = "mm/dd/yyyy" }
                $(element).fdatepicker({format: scope.format}).on('changeDate', function(ev){

                    scope.$apply(function(){
                        ngModel.$setViewValue(ev.date);
                    });
                })
            }
        }
    });





angular.module('timerApp').factory("timerListModel", ["$interval", "$http", function($interval, $http) {
    var model = {};
    model.theInterval = undefined;


    /*model.userId = "561dcd3c8c57cf2c17b7f4f9";
    if(g_userId != '') {
        model.userId = g_userId;
    }
    */
    model.scriptParams = scriptParams;
    /*model.userId = scriptParams.userId;
    model.authToken = scriptParams.userId;
    model.userEmail = g_userEmail;
*/
    var scripts = document.getElementsByTagName('script');
    var lastScript = scripts[scripts.length - 1];
    var scriptName = lastScript;

    model.timers = [];
    model.$scope = null;

    model.setScope = function(scope) {
        model.$scope = scope;
    }

    model.getAuthorizationHeader = function() {
        auth = model.scriptParams.userEmail + ':' + model.scriptParams.authToken
        return 'Basic ' + btoa(auth);
    }

    model.startTimer = function() {
        if ( angular.isDefined(model.theInterval) )
            return;
        model.theInterval = $interval(model.onIntervalTick, 1000);
        model.timers[0].running = true;
        model.saveTimerToServer(0);
    }

    model.stopTimer = function() {

        if ( angular.isDefined(model.theInterval) ) {
            $interval.cancel(model.theInterval);
        }
        model.theInterval = undefined;
        if(model.timers.length > 0 && model.timers[0].running == true) {
            model.timers[0].running = false;
            model.saveTimerToServer(0);
        }
    }

    model.totalTimerTime = function(index) {
        return model.timers[index].seconds;
    }

    model.onIntervalTick = function() {
        model.timers[0].seconds++;
    }

    model.activateTimer = function (index) {
        t = model.timers[index];
        model.timers.splice(index, 1);
        t.lastRestart = new Date().toISOString();
        t.lastRestart = t.lastRestart;
        model.timers.unshift(t);
        model.saveTimerToServer(0);
    }

    model.deleteTimer = function(index) {
        console.log(model.timers[index].id);
        $http({
            method: 'DELETE',
            url: '/api/v1/timer/' + model.timers[index].id,
            headers: {
                'Authorization': model.getAuthorizationHeader()
            }
        }).then(function successCallback(response) {
            console.log("Delete successful.");
            model.timers.splice(index, 1);
        }, function errorCallback(response) {
            console.log(response);
            //alert("Unable to delete timer");
        });
    }

    model.saveTimerToServer = function(index) {
        console.log("saveTimerToServer with index = " + index);
        //console.log("Before save: " + JSON.stringify(model.timers[index], null, 4));
        $http({
            method: 'POST',
            headers: {
                'Authorization': model.getAuthorizationHeader()
            },
            url: '/api/v1/timer',
            data: model.timers[index]
        }).then(function successCallback(response) {
            model.timers[index] = response.data;
          //  console.log("After save: " + JSON.stringify(model.timers[index], null, 4));
        }, function errorCallback(response) {
            console.log(response);
            alert("Unable to save timer");
        });
    }

    model.getMidnightTodayAsString = function () {
        d = new Date();
        d2 = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 0,0,0,0);
        return d2.toISOString();
    }

    model.getDefaultTimer = function() {
        timer = {
            "dateEntered": model.getMidnightTodayAsString(),
            "seconds": 0,
            "lastRestart": model.getMidnightTodayAsString(),
            "notes": "",
            "tags" : [],
            "running": false,
            "user": model.scriptParams.userId
        };
        return timer;
    }

    model.init = function() {
        console.log("Inside init...");
        $http({
            method: 'GET',
            headers: {
                'Authorization': model.getAuthorizationHeader()
            },
            url: '/api/v1/timer'
        }).then(function successCallback(response) {
            model.timers = response.data.timers;
            if (model.timers.length == 0) {
                model.createNewTimer();
            }
        }, function errorCallback(response) {
            alert("Unable to get timers from server ");
            console.log(response);
        });
    }

    model.createNewTimer = function() {
        model.timers.unshift(model.getDefaultTimer());

    }

    return model;
}]);

angular.module('timerApp').controller('TimerController', ['$scope', 'timerListModel', function($scope, timerListModel) {
    //$scope.someTimerValue = 99;
    //$scope.timeFormatter = new TimeFormatter();
    $scope.timeFormatted = "0:00:00" ; // $scope.timeFormatter.formatSeconds(1);
    $scope.startButtonClass = "success";
    $scope.startButtonText = "Start";
    $scope.timers_json = $scope.timers;
    $scope.startDisplayed = true;
    $scope.timerListModel = timerListModel;
    $scope.timerListModel.setScope($scope);
    $scope.timerClass = " ";

    $scope.startTimer = function()  {
        console.log("$scope.startTimer");
        $scope.startButtonClass = "alert";
        $scope.startButtonText = "Stop";
        $scope.timerListModel.startTimer();
        $scope.startEnabled = false;
        $scope.stopEnabled = true;
        $scope.timerClass = "runningTimer"
    }
    $scope.stopTimer = function()  {
        $scope.timerClass = " ";
        console.log("$scope.stopTimer");
        $scope.startButtonText = "Start";
        $scope.startButtonClass = "success";
        $scope.startEnabled = true;
        $scope.stopEnabled = false;
        $scope.timerListModel.stopTimer();
    }

    $scope.toggleTimer = function() {
        if (! $scope.timerListModel.timers[0].running ) {
            $scope.startTimer();
        }
        else {
            $scope.stopTimer();
        }
    }
    $scope.$watch('startDisplayed', function(){
        $scope.startDisplayed ?  $scope.stopTimer() : $scope.startTimer() ;
    });

    $scope.activateTimer = function(index) {
        $scope.stopTimer();
        //$scope.timerListModel.activateTimer(index);
        setTimeout(function() {
            $scope.timerListModel.activateTimer(index);
            $scope.$apply(); //this triggers a $digest
        }, 500);
    }

    // TODO if active LegacyTimer, should stop it first?
    $scope.deleteTimer = function(index) {
        if(confirm("Delete timer, are you sure?")) {
            setTimeout(function () {
                if (index == 0) {
                    $scope.stopTimer();
                }
                $scope.timerListModel.deleteTimer(index);
                $scope.$apply(); //this triggers a $digest
            }, 500);
        }
    }


    $scope.isEmpty = function(input) {
        return (angular.equals(input,null) || angular.equals(input,''));
    }

    $scope.timerListModel.init();

    $scope.createNewTimer = function() {
        $scope.stopTimer();
        setTimeout(function() {
            $scope.timerListModel.timers.unshift($scope.timerListModel.getDefaultTimer());
            $scope.$apply(); //this triggers a $digest
        }, 500);
    }

    $scope.noOp = function() {
        console.log("noOp");
    }

    $scope.getLatestTimerDate = function(timer) {
        var longDate = timer.dateEntered;

        //return longDate;

        var mm = longDate.substr(5,2);
        var yyyy = longDate.substr(0, 4);
        var dd = longDate.substr(8,2);

        return mm + "/" + dd + "/" + yyyy;

    }

}]);

