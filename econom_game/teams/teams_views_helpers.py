from .models import Team


def is_in_database(new_team):
    teams_database = Team.objects.all()
    if new_team in teams_database:
        return True
    return False
