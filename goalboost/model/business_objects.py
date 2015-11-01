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

class PacificTimeConverter:
    @classmethod
    def naive_utc_to_pacific_time(cls, pacific):
        return "Foobar"