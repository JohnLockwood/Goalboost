
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
        else {
            timeStr = pad("0", 1, 0) + ":" + timeStr;
        }
        return timeStr; // + " " + suffix;
    }
});

// angular.directive('timerApp')
angular.module('timerApp').directive('timeEntry', function($log) {
    return {
        require: 'ngModel',
        link: function(scope, element, attrs, ngModelCtrl) {

            ngModelCtrl.$formatters.push(
                function (timeInSeconds) {
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
                    else {
                        timeStr = pad("0", 1, 0) + ":" + timeStr;
                    }
                    $log.log("Value " + timeInSeconds + " formatted to " + timeStr);
                    return timeStr; // + " " + suffix;
                });

            ngModelCtrl.$parsers.push(function(value) {
                tokens= value.split(":");
                if (tokens.length == 3) {
                    if (tokens[0].length > 0 && tokens[1].length > 0 && tokens[2].length > 0) {
                      var hours = parseInt(tokens[0]);
                        var minutes = parseInt(tokens[1]);
                        var seconds = parseInt(tokens[2]);
                        return (hours * 3600) + (minutes * 60) + seconds;
                    }
                }
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


            link: function(scope, element, attrs, ngModel){

                if(typeof(scope.format) == "undefined"){ scope.format = "mm/dd/yyyy" }
                $(element).fdatepicker({format: scope.format}).on('changeDate', function(ev){
                    scope.$apply(function(){
                        ngModel.$setViewValue(ev.date);
                    });
                });
            }
        }
    });


/*angular.module('timerApp').directive('timeEntry',
    function TimeEntry($log){
        return {
            require: 'ngModel',
            restrict: 'A',
            templateUrl: "time-entry-display.html",
            replace: true,
            //template:  '<div class="large-8 columns" >Hello world</div>',
            //template: "Hello",
            link: function(scope, element, attrs, ngModel) {
                //$log.log("" + ngModel);
                //$log.log(element.html());
            }
        }
    });
*/



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
        timer = model.timers[index];

        if (typeof(timer.id) == "undefined") {
            model.timers.splice(index, 1);
        }
        else {
            $http({
                method: 'DELETE',
                url: '/api/v1/timer/' + timer.id,
                headers: {
                    'Authorization': model.getAuthorizationHeader()
                }
            }).then(function successCallback(response) {
                console.log("Delete successful.");
                model.timers.splice(index, 1);
            }, function errorCallback(response) {
                //console.log(response);
                alert("Unable to delete timer");
            });
        }
    }

    model.saveTimerToServer = function(index) {
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

    model.zeropad = function(s) {
        if (s.length == 1) {
            s = "0" + s;
        }
        return(s);
    }

    model.getMidnightTodayAsString = function () {
        d = new Date();
        month = this.zeropad("" + (d.getMonth() + 1));
        day =  this.zeropad("" + d.getDate());
        year = "" + d.getFullYear();
        return month + "/" + day + "/" + year;
        //return d2.toISOString();
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
        // console.log("Inside init...");
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
    $scope.startButtonClass = "success fi-play";
    $scope.startButtonText = "Start";
    $scope.timers_json = $scope.timers;
    $scope.startDisplayed = true;
    $scope.timerListModel = timerListModel;
    $scope.timerListModel.setScope($scope);
    $scope.timerClass = " ";

    $scope.startTimer = function()  {
        // console.log("$scope.startTimer");
        $scope.startButtonClass = "alert fi-pause";
        $scope.startButtonText = "Stop";
        $scope.timerListModel.startTimer();
        $scope.startEnabled = false;
        $scope.stopEnabled = true;
        $scope.timerClass = "runningTimer"
    }
    $scope.stopTimer = function()  {
        $scope.timerClass = " ";
        // console.log("$scope.stopTimer");
        $scope.startButtonText = "Start";
        $scope.startButtonClass = "success fi-play";
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

/* ngTagEditor

 */


angular.module('timerApp')
    .filter('getCol', function(){
        return function (items, row){
            return items && items.map(function (item){
                    return item[row];
                }).join(',');
        }
    }).directive('focusMe', ['$timeout', '$parse', function($timeout, $parse){
    return{
        link: function(scope, element, attrs){
            var model = $parse(attrs.focusMe);
            scope.$watch(model, function(value){
                if(value === true){
                    $timeout(function(){
                        element[0].focus();
                    });
                }
            });
            element.bind('blur', function(){
                scope.$apply(model.assign(scope, false));
            });
        }
    };
}]).directive('tagEditor', function(){
    return{
        restrict: 'AE',
        /* require: 'ngModel',*/
        scope: {
            tags: '=ngModel'
        },
        replace: true,
        templateUrl: 'ngTagEditor.html',
        controller: ['$scope', '$attrs', '$element', '$http', '$filter', function($scope, $attrs, $element, $http, $filter){

            $scope.options = [];
            $scope.options.output = $attrs.output || 'name';
            $scope.options.fetch = $attrs.fetch || 'suggestions.php?q=';
            $scope.options.placeholder = $attrs.placeholder || 'Enter a few letters...';
            $scope.options.apiOnly = $attrs.apiOnly || false;
            $scope.search = '';

            $scope.$watch('search', function(){
                /*$http.get($scope.options.fetch + $scope.search).success(function(data){
                    $scope.suggestions = data.data;
                    //  console.log(data);
                });
            */
            });
            $scope.add = function(id, name){
                $scope.tags.push(name);
                $scope.search = '';
                $scope.$apply();
            };
            $scope.remove = function(index){
                $scope.tags.splice(index, 1);
            };

            $element.find('input').on('keydown', function(e){
                var keys = [8, 13, 32];
                if(keys.indexOf(e.which) !== -1){
                    if(e.which == 8){ /* backspace */
                        if($scope.search.length === 0 && $scope.tags.length){
                            $scope.tags.pop();
                            e.preventDefault();
                        }
                    }
                    else if(e.which == 32 || e.which == 13){ /* space & enter */
                        if($scope.search.length && !$scope.apiOnly){
                            if(!$scope.apiOnly){
                                $scope.add(0, $scope.search);
                                e.preventDefault();
                            }
                        }
                    }
                    $scope.$apply();
                }
            });

        }]
    }
});