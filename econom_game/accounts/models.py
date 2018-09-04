from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _

from stations.models import Station
from banks.models import Bank


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        permissions = (
            (
                "add_station",
                "Can view '/admin/add_station/' page"
            ),
            (
                "add_group",
                "Can view '/admin/add_group/' page"
            ),
            (
                "view_shares",
                "Can view '/admin/shares/' page"
            ),
            (
                "view_confirm_transaction",
                "Can view '/admin/confirm_transaction/' page"
            ),
            (
                "view_give_money",
                "Can view '/admin/give_money/' page"
            ),
            (
                "view_exclude_money",
                "Can view '/admin/exclude_money/' page"
            ),
        )


class StationAdmin(models.Model):
    station = models.ForeignKey(Station, related_name='station', default=None)
    user = models.OneToOneField(User)

    class Meta:
        permissions = (
            ("view_station", "Can view '/admin/station/' page"),
        )

    def __str__(self):
        return '%s admin' % self.station.name


class Operator(models.Model):
    bank = models.ForeignKey(Bank, related_name='bank', default=None)
    user = models.OneToOneField(User)

    class Meta:
        permissions = (
            ("view_deposit", "Can view '/admin/deposit/' page"),
            ("view_credit", "Can view '/admin/credit/' page"),
            ("view_give_money", "Can view '/admin/give_money/' page"),
            (
                "view_confirm_transaction",
                "Can view '/admin/confirm_transaction/' page"
            ),
            (
                "add_group",
                "Can view '/admin/add_group/' page"
            ),
        )

    def __str__(self):
        return '%s bank operator' % self.bank.name


class Financier(models.Model):
    user = models.OneToOneField(User)

    class Meta:
        permissions = (
            ("view_shares", "Can view '/admin/shares/' page"),
        )

    def __str__(self):
        return '%s' % self.user.first_name
