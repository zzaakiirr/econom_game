from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist

from stations.models import Station
from accounts.models import User, StationAdmin


@receiver(post_save, sender=Station)
def create_station_admin(sender, instance, created, **kwargs):
    if created and not is_station_admin_already_exist(instance):
        email = 'station_admin_%d' % instance.id

        user = User.objects.create(email=email, password=email)
        StationAdmin.objects.create(
            station=instance, user=user
        )


def is_station_admin_already_exist(instance):
    station_admin = StationAdmin.objects.filter(station=instance)
    if len(station_admin):
        return False
    return True
