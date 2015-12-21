from goalboost.model.timer_models import Timer
from datetime import datetime

def add_timer_to_user():
    pass

# Todo we need a user here
def create_timer(userId=None, startTime=datetime.utcnow(), **kwargs):
    timer = Timer(userId=userId, startTime=startTime, **kwargs)
    return timer

# JCL review exceptions and return values
class TimerDao:
    # JCL review exceptions
    def timer_by_id(self, id):
        return Timer.objects(id = id).first()

    # JCL review exceptions and return values
    def timers_for_user(self, user_id):
        return [t for t in Timer.objects(userId = user_id).order_by("-lastRestart").all()]

    # JCL todo handle exception
    def save_timer(self, timer):
        timer.save()

    # Returns true if the timer is found and deleted.  False for not found.
    # Return value currently ignored by API
    def delete_timer(self, timer_id):
        timer = Timer.objects(id = timer_id).first()
        if (timer):
            # Todo can this still throw exception
            timer.delete()
            return True
        else:
            return False