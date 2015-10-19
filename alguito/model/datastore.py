from .mongo_models import Timer
from datetime import datetime

def add_timer_to_user():
    pass

# Todo we need a user here
def create_timer(userId=None, startTime=datetime.utcnow(), **kwargs):
    timer = Timer(userId, startTime, **kwargs)
    return timer