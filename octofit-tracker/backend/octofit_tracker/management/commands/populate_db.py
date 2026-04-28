from datetime import datetime, date
from django.core.management.base import BaseCommand
from django.utils import timezone
from pymongo import MongoClient
from octofit_tracker.models import Activity, LeaderboardEntry, Team, User, Workout


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting existing data...')
        Activity.objects.all().delete()
        LeaderboardEntry.objects.all().delete()
        Workout.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel', description='Team Marvel superheroes')
        dc = Team.objects.create(name='DC', description='Team DC superheroes')

        self.stdout.write('Creating users...')
        users = [
            User.objects.create(first_name='Peter', last_name='Parker', email='peter.parker@marvel.com', team=marvel, super_hero_name='Spider-Man'),
            User.objects.create(first_name='Tony', last_name='Stark', email='tony.stark@marvel.com', team=marvel, super_hero_name='Iron Man'),
            User.objects.create(first_name='Bruce', last_name='Wayne', email='bruce.wayne@dc.com', team=dc, super_hero_name='Batman'),
            User.objects.create(first_name='Diana', last_name='Prince', email='diana.prince@dc.com', team=dc, super_hero_name='Wonder Woman'),
        ]

        self.stdout.write('Creating activities...')
        Activity.objects.create(
            user=users[0],
            team=marvel,
            activity_type='Running',
            duration_minutes=45,
            distance_km=8.3,
            performed_at=timezone.make_aware(datetime(2026, 4, 27, 10, 30)),
        )
        Activity.objects.create(
            user=users[1],
            team=marvel,
            activity_type='Cycling',
            duration_minutes=60,
            distance_km=20.1,
            performed_at=timezone.make_aware(datetime(2026, 4, 27, 8, 0)),
        )
        Activity.objects.create(
            user=users[2],
            team=dc,
            activity_type='Swimming',
            duration_minutes=30,
            distance_km=1.2,
            performed_at=timezone.make_aware(datetime(2026, 4, 26, 17, 15)),
        )
        Activity.objects.create(
            user=users[3],
            team=dc,
            activity_type='Yoga',
            duration_minutes=50,
            distance_km=None,
            performed_at=timezone.make_aware(datetime(2026, 4, 26, 19, 0)),
        )

        self.stdout.write('Creating leaderboard entries...')
        LeaderboardEntry.objects.create(user=users[0], team=marvel, score=1200, rank=1, category='Endurance')
        LeaderboardEntry.objects.create(user=users[1], team=marvel, score=1150, rank=2, category='Strength')
        LeaderboardEntry.objects.create(user=users[2], team=dc, score=1220, rank=1, category='Endurance')
        LeaderboardEntry.objects.create(user=users[3], team=dc, score=1100, rank=2, category='Flexibility')

        self.stdout.write('Creating workouts...')
        Workout.objects.create(
            user=users[0],
            title='Web-Swing Warmup',
            description='High-intensity interval training for agility.',
            duration_minutes=30,
            calories_burned=320,
            scheduled_date=date(2026, 4, 29),
        )
        Workout.objects.create(
            user=users[1],
            title='Arc Reactor Strength',
            description='Full-body strength session.',
            duration_minutes=40,
            calories_burned=410,
            scheduled_date=date(2026, 4, 29),
        )
        Workout.objects.create(
            user=users[2],
            title='Night Patrol',
            description='Endurance run with extra core work.',
            duration_minutes=55,
            calories_burned=480,
            scheduled_date=date(2026, 4, 30),
        )
        Workout.objects.create(
            user=users[3],
            title='Amazonian Recovery',
            description='Yoga and mobility to recover from training.',
            duration_minutes=35,
            calories_burned=210,
            scheduled_date=date(2026, 4, 30),
        )

        self.stdout.write('Creating unique email index...')
        client = MongoClient('mongodb://127.0.0.1:27017')
        client.octofit_db.users.create_index([('email', 1)], unique=True)
        client.close()

        self.stdout.write(self.style.SUCCESS('octofit_db has been populated with test data.'))
