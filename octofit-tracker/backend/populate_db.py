"""
populate_db.py

This script populates the OctoFit Tracker database with initial data for development and testing.
It uses Django's ORM and should be run from the backend directory with the virtual environment activated.

Usage:
    source venv/bin/activate
    python manage.py shell < populate_db.py
"""

from octofit_tracker.models import user, team, activity, workout, leaderboard
from django.contrib.auth import get_user_model

User = get_user_model()

# Create users
def create_users():
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

# Create teams
def create_teams(users):
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

# Create workouts
def create_workouts():
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

# Create activities
def create_activities(users, workouts):
    activities = [
        {"user": users[0], "workout": workouts[0], "duration": 10, "calories": 50},
        {"user": users[1], "workout": workouts[1], "duration": 30, "calories": 200},
        {"user": users[2], "workout": workouts[2], "duration": 5, "calories": 30},
    ]
    for a in activities:
        activity.Activity.objects.create(user=a["user"], workout=a["workout"], duration=a["duration"], calories=a["calories"])

# Create leaderboard entries
def create_leaderboard():
    leaderboard.update_leaderboard()

if __name__ == "__main__":
    users = create_users()
    teams = create_teams(users)
    workouts = create_workouts()
    create_activities(users, workouts)
    create_leaderboard()
    print("Database populated with initial data.")
