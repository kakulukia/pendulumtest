import pendulum as pendulum
from django.test import TestCase

from .models import Event


class PendulumTest(TestCase):

    def setUp(self):
        self.now = pendulum.now().start_of('day')
        self.event = Event.objects.create(start=self.now)

    def test_datetime_query(self):

        self.assertEqual(Event.objects.filter(start=self.now).count(), 1)

        self.event.refresh_from_db()
        self.event.save()
        # now the text representation in the DB changed to datetime.datetime

        # and tho being treated as the same time
        self.assertEqual(self.event.start, self.now)

        # the ORM cant find my event anymore
        self.assertEqual(Event.objects.filter(start=self.now).count(), 1)

    def test_dates_query(self):

        # this is not working since the django function that is filtering out the dates
        # cant handle pendulums datetime strings i guess
        years = Event.objects.dates('start', 'year')
        self.assertIn(pendulum.datetime(2018, 1, 1).date(), years)

        # but it will work if we do this and test it again
        self.event.refresh_from_db()
        self.event.save()

        years = Event.objects.dates('start', 'year')
        self.assertIn(pendulum.datetime(2018, 1, 1).date(), years)

    def test_weird_time_difference(self):

        self.event.refresh_from_db()
        self.event.save()

        # now it get even more weird
        # we have exactly one event in the database
        self.assertEqual(Event.objects.count(), 1)

        # and the events start time matches, what we used to save it with
        self.assertEqual(Event.objects.get().start, self.now)

        # so this should not be possible
        self.assertEqual(Event.objects.filter(start__range=(
            self.now.subtract(hours=22, minutes=59),
            self.now.subtract(hours=22))).count(), 0, 'wen shouldnt have an event here')
