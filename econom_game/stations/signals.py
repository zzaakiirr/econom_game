from django.db.models.signals import post_save
from django.dispatch import receiver

from stations.models import Station
from accounts.models import User, StationAdmin


@receiver(post_save, sender=Station)
def create_station_admin(sender, instance, created, **kwargs):
    if created:
        email = 'station_admin_%d' % instance.id

        user = User.objects.create(email=email, password=email)
        StationAdmin.objects.create(
            station=instance, user=user
        )
