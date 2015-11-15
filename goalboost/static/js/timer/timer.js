var timerApp = angular.module('timerApp', []);

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
            // suffix = "minutes";
        }
        else {
            timeStr = pad("00", 2, 0) + ":" + timeStr;
        }
        if (timeInSeconds >= 3600) {
            hours = Math.floor(timeInSeconds / 3600);
            timeStr = hours + ":" + timeStr;
            //  suffix = "hours";
        }

        return timeStr; // + " " + suffix;
    }
});

angular.module('timerApp').factory("timerListModel", ["$interval", function($interval) {
    var model = {};
    model.testlist = ["foo", "bar"];
    model.theInterval = undefined;
    model.timers = [
        {
            "entries": [
                {
                    "dateRecorded": "2015-11-14 00:00:00",
                    "seconds": 0
                }
            ],
            "id": "56475cec8c57cf58c9d4cf52",
            "lastRestart": "2015-11-14T16:10:20.892000",
            "notes": "Enter a task",
            "running": true,
            "startTime": "2015-11-14T16:10:20.892000",
            "userId": "56259a278c57cf02f9692b31"
        },
        {
            "entries": [
                {
                    "dateRecorded": "2015-11-13 00:00:00",
                    "seconds": 300
                }
            ],
            "id": "5646c29a8c57cf4c1b2e74c1",
            "lastRestart": "2015-11-14T05:11:54.138000",
            "notes": "Saving the world",
            "running": true,
            "startTime": "2015-11-14T05:11:54.138000",
            "userId": "56259a278c57cf02f9692b31"
        },
        {
            "entries": [
                {
                    "dateRecorded": "2015-11-13 00:00:00",
                    "seconds": 900
                }
            ],
            "id": "5645fe398c57cf5b8991f377",
            "lastRestart": null,
            "notes": "Curing the Internet",
            "running": true,
            "startTime": null,
            "userId": "56259a278c57cf02f9692b31"
        }
    ];

    model.startTimer = function() {
        //console.log("timerListModel::startTimer");
        if ( angular.isDefined(model.theInterval) )
            return;
        model.theInterval = $interval(model.onIntervalTick, 1000);
    }

    model.stopTimer = function() {
        // console.log("timerListModel::stopTimer");
        $interval.cancel(model.theInterval);
        model.theInterval = undefined;
    }

    model.onIntervalTick = function() {
        // console.log("Tick...");
        model.timers[0].entries[0].seconds++;
    }
    return model;
}]);

angular.module('timerApp').controller('TimerController', ['$scope',  'timerListModel', function($scope, timerListModel) {
    //$scope.someTimerValue = 99;
    //$scope.timeFormatter = new TimeFormatter();
    $scope.timeFormatted = "0:00:00" ; // $scope.timeFormatter.formatSeconds(1);

    $scope.startButtonClass = "success";
    $scope.startButtonText = "Start";
    $scope.timers_json = $scope.timers;
    $scope.startDisplayed = true;
    $scope.timerListModel = timerListModel;

    $scope.startTimer = function()  {
        $scope.startButtonClass = "alert";
        $scope.startButtonText = "Stop";
        $scope.timerListModel.startTimer();
    }
    $scope.stopTimer = function()  {
        $scope.startButtonText = " Start ";
        $scope.startButtonClass = "success";
        $scope.timerListModel.stopTimer();
    }

    $scope.$watch('startDisplayed', function(){
        $scope.startDisplayed ?  $scope.stopTimer() : $scope.startTimer() ;
    });

}]);
