from goalboost.model.mongo_models import Timer

class UserTimer:
    def __init__(self, user, db):
        self.user = user
        if self.user.timer is not None:
            timerid = self.user.timer
            query_set = Timer.objects(id = self.user.timer)
            try:
                self.user.timer = query_set.first()
            except:
                self.user.timer = None
        self.db = db

    def timer_get(self):
        return self.user.timer

    def timer_get_timer_object(self):
        pass

    def timer_create(self):
        self.timer = Timer(userId = self.user.id)
        self.timer.save()
        self.user.timer = self.timer.id
        self.user.save()
        return self.timer

    def timer_clear(self):
        self.timer = None
        self.user.timer = None
        self.user.save()

class TimerDao:
    def timer_by_id(self, id):
        return Timer.objects(id = id).first()

    def timers_for_user(self, user_id):
        return [t for t in Timer.objects(userId = user_id).order_by("-lastRestart").all()]

    def save_timer(self, timer):
        timer.save()