from unittest import TestCase
from alguito.model.datastore import create_timer
from datetime import datetime

class TestTimer(TestCase):
    def test_can_create_with_utc_now(self):
        userId = "561dcd3c8c57cf2c17b7f4f9"
        my_notes = "I want to know how long this took, but my code is brain dead so far.  Woe is me."
        timer = create_timer(notes=my_notes, userId=userId)
        assert(my_notes == timer.notes)
        timer.save()

    def test_can_create_with_explicit_start(self):
        my_notes = "I am another timer"
        timer = create_timer(notes=my_notes, startTime=datetime(2007, 12, 5, 0, 0))
        assert(my_notes == timer.notes)
