"""
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
    help = 'Populates the database with initial data for development and testing.'

    def handle(self, *args, **options):
        users = self.create_users()
        teams = self.create_teams(users)
        workouts = self.create_workouts()
        self.create_activities(users, workouts)
        self.create_leaderboard()
        self.stdout.write(self.style.SUCCESS('Database populated with initial data.'))

    def create_users(self):
        users = [
            {"username": "alice", "email": "alice@example.com", "password": "password123"},
            {"username": "bob", "email": "bob@example.com", "password": "password123"},
            {"username": "carol", "email": "carol@example.com", "password": "password123"},
        ]
        user_objs = []
        for u in users:
            obj, created = User.objects.get_or_create(username=u["username"], defaults={"email": u["email"]})
            if created:
                obj.set_password(u["password"])
                obj.save()
            user_objs.append(obj)
        return user_objs

    def create_teams(self, users):
        teams = [
            {"name": "Team Alpha", "members": [users[0], users[1]]},
            {"name": "Team Beta", "members": [users[2]]},
        ]
        team_objs = []
        for t in teams:
            obj, created = team.Team.objects.get_or_create(name=t["name"])
            obj.members.set(t["members"])
            obj.save()
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
