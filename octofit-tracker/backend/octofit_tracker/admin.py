from django.contrib import admin
from .models.user import User
from .models.team import Team
from .models.activity import Activity
from .models.leaderboard import Leaderboard
from .models.workout import Workout

admin.site.register(User)
admin.site.register(Team)
admin.site.register(Activity)
admin.site.register(Leaderboard)
admin.site.register(Workout)
