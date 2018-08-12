from django.db import models


class Group(models.Model):
    class Meta:
        permissions = (
            ("view_station", "Can view '/station' page"),
        )
