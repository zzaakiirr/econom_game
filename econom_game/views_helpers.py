from teams.models import Team, Card
from stations.models import Station
from teams.models import Team, Card


def is_in_database(new_object):
    if new_object._state.db:
        return True
    return False
