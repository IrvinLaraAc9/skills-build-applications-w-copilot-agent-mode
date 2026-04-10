"""
Populate the octofit_db database with test data
Custom Django management command to populate the OctoFit Tracker database with initial data.
Usage:
    source venv/bin/activate
    python manage.py populate_db
"""

from django.core.management.base import BaseCommand
from octofit_tracker.models import user, team, activity, workout, leaderboard
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data.'

    def handle(self, *args, **options):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        # Delete all data
        activity.Activity.objects.all().delete()
        workout.Workout.objects.all().delete()
        team.Team.objects.all().delete()
        User.objects.all().delete()
        # Create teams Marvel and DC
        self.create_teams()
        # Create users (superheroes)
        users = self.create_users()
        # Create workouts
        workouts = self.create_workouts()
        # Create activities
        self.create_activities(users, workouts)
        # Update leaderboard
        self.create_leaderboard()
        self.stdout.write(self.style.SUCCESS('Database populated with initial data.'))

    def create_users(self):
        from django.contrib.auth import get_user_model
        User = get_user_model()
        users = [
            {"username": "superman", "email": "superman@dc.com", "password": "krypton", "is_superuser": True, "is_superhero": True, "team": "DC"},
            {"username": "batman", "email": "batman@dc.com", "password": "wayne", "is_superhero": True, "team": "DC"},
            {"username": "wonderwoman", "email": "wonderwoman@dc.com", "password": "amazon", "is_superhero": True, "team": "DC"},
            {"username": "ironman", "email": "ironman@marvel.com", "password": "stark", "is_superhero": True, "team": "Marvel"},
            {"username": "spiderman", "email": "spiderman@marvel.com", "password": "parker", "is_superhero": True, "team": "Marvel"},
            {"username": "captainmarvel", "email": "captainmarvel@marvel.com", "password": "carol", "is_superhero": True, "team": "Marvel"},
        ]
        user_objs = []
        for u in users:
            obj, created = User.objects.get_or_create(username=u["username"], defaults={"email": u["email"], "team": u["team"]})
            if created:
                obj.set_password(u["password"])
                obj.is_superuser = u.get("is_superuser", False)
                obj.is_superhero = u.get("is_superhero", False)
                obj.save()
            user_objs.append(obj)
        return user_objs

    def create_teams(self):
        teams = [
            {"name": "Marvel", "description": "Marvel superheroes"},
            {"name": "DC", "description": "DC superheroes"},
        ]
        team_objs = []
        for t in teams:
            obj, created = team.Team.objects.get_or_create(name=t["name"], defaults={"description": t["description"]})
            team_objs.append(obj)
        return team_objs

    def create_workouts(self):
        workouts = [
            {"name": "Push Ups", "description": "Do 20 push ups"},
            {"name": "Running", "description": "Run 2 miles"},
            {"name": "Plank", "description": "Hold plank for 1 minute"},
        ]
        workout_objs = []
        for w in workouts:
            obj, _ = workout.Workout.objects.get_or_create(name=w["name"], defaults={"description": w["description"]})
            workout_objs.append(obj)
        return workout_objs

    def create_activities(self, users, workouts):
        activities = [
            {"user": users[0], "workout": workouts[0], "duration": 10, "calories": 50},
            {"user": users[1], "workout": workouts[1], "duration": 30, "calories": 200},
            {"user": users[2], "workout": workouts[2], "duration": 5, "calories": 30},
        ]
        for a in activities:
            activity.Activity.objects.create(user=a["user"], workout=a["workout"], duration=a["duration"], calories=a["calories"])

    def create_leaderboard(self):
        leaderboard.update_leaderboard()
