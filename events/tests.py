import pendulum as pendulum
from django.test import TestCase

from .models import Event


class PendulumTest(TestCase):

    def test_datetime_query(self):
        now = pendulum.now()

        event = Event.objects.create(start=now)
        self.assertEqual(Event.objects.filter(start=now).count(), 1)

        event.refresh_from_db()
        event.save()

        # now its different because the text representation in the DB changed to
        # the datetime.datetime version
        self.assertEqual(Event.objects.filter(start=now).count(), 1)

    def test_dates_query(self):

        now = pendulum.now()

        event = Event.objects.create(start=now)

        # this is not working since the django function that is filtering out the dates
        # cant handle pendulums datetime strings i guess
        years = Event.objects.dates('start', 'year')
        self.assertIn(pendulum.datetime(2018, 1, 1).date(), years)

        # but it will work if we do this and test it again
        event.refresh_from_db()
        event.save()

        years = Event.objects.dates('start', 'year')
        self.assertIn(pendulum.datetime(2018, 1, 1).date(), years)
