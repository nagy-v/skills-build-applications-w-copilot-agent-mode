from django.core.management.base import BaseCommand
from apps.tracker.models import User, Team, Activity, Leaderboard, Workout
from django.utils import timezone

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear existing data
        Leaderboard.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Team.objects.all().delete()
        User.objects.all().delete()

        # Create users (superheroes)
        users_data = [
            {'email': 'tony@marvel.com', 'username': 'IronMan', 'first_name': 'Tony', 'last_name': 'Stark'},
            {'email': 'steve@marvel.com', 'username': 'CaptainAmerica', 'first_name': 'Steve', 'last_name': 'Rogers'},
            {'email': 'bruce@marvel.com', 'username': 'Hulk', 'first_name': 'Bruce', 'last_name': 'Banner'},
            {'email': 'clark@dc.com', 'username': 'Superman', 'first_name': 'Clark', 'last_name': 'Kent'},
            {'email': 'bruce@dc.com', 'username': 'Batman', 'first_name': 'Bruce', 'last_name': 'Wayne'},
            {'email': 'diana@dc.com', 'username': 'WonderWoman', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]
        users = []
        for data in users_data:
            u = User.objects.create(**data)
            users.append(u)

        # Create teams
        marvel = Team.objects.create(name='marvel', description='Marvel heroes')
        dc = Team.objects.create(name='dc', description='DC heroes')
        marvel.members.add(*users[:3])
        dc.members.add(*users[3:])

        # Create activities
        Activity.objects.create(user=users[0], activity_type='running', duration_minutes=30, date=timezone.now().date())
        Activity.objects.create(user=users[1], activity_type='cycling', duration_minutes=45, date=timezone.now().date())
        Activity.objects.create(user=users[2], activity_type='gym', duration_minutes=60, date=timezone.now().date())
        Activity.objects.create(user=users[3], activity_type='running', duration_minutes=25, date=timezone.now().date())
        Activity.objects.create(user=users[4], activity_type='swimming', duration_minutes=40, date=timezone.now().date())
        Activity.objects.create(user=users[5], activity_type='yoga', duration_minutes=50, date=timezone.now().date())

        # Leaderboard entries
        for u in users:
            team = marvel if u in marvel.members.all() else dc
            Leaderboard.objects.create(user=u, team=team, total_activities=1, total_calories=100, total_distance_km=5.0, total_minutes=30, rank=1)

        # Workouts
        Workout.objects.create(name='Full Body Blast', description='Intense full body workout', duration_minutes=45, difficulty='hard', exercises=['pushups','squats','burpees'])
        Workout.objects.create(name='Morning Yoga', description='Gentle stretching and breathing', duration_minutes=30, difficulty='easy', exercises=['sun salutations','child pose'])

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
