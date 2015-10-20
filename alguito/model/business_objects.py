from alguito.model.mongo_models import Timer

class UserTimer:
    def __init__(self, user, db):
        self.user = user
        if self.user.timer is not None:
            self.timer = Timer.find(id = self.user.timer)
        self.db = db

    def timer_get(self):
        return self.user.timer

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