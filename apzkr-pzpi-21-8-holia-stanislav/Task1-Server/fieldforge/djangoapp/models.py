from django.contrib.gis.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import uuid
import pytz
import jwt
from datetime import datetime, timedelta
from django.conf import settings 
from django.forms.models import model_to_dict

from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# Custom user manager
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, role, password=None, **extra_fields):
        # Check for required fields
        if email is None:
            raise TypeError('Users must have an email address.')
        if first_name is None:
            raise TypeError('Users must have a first name.')
        if last_name is None:
            raise TypeError('Users must have a last name.')
        if role is None:
            raise TypeError('Users must have a role.')
        if role not in ['INSTRUCTOR', 'SOLDIER']:
            raise ValueError('Role must be either "INSTRUCTOR" or "SOLDIER".')

        try:
            if role == 'INSTRUCTOR':
                 return self.create_instructor(email,first_name, last_name, password, role, **extra_fields)
            elif role == 'SOLDIER':
                 return self.create_soldier(email,first_name, last_name, password, role, **extra_fields)
        except ValueError:
            raise

    def create_admin(self, email, first_name, last_name, password=None):
        # Check for required fields
        if email is None:
            raise TypeError('Users must have an email address.')
        if first_name is None:
            raise TypeError('Users must have a first name.')
        if last_name is None:
            raise TypeError('Users must have a last name.')

        user = User(email=self.normalize_email(email=email),first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.is_staff = True
        user.save()

        return user

    def create_instructor(self, email, first_name, last_name, password,role, **extra_fields):
        instructor_fields = {k: v for k, v in extra_fields.items() if k in ['experience', 'specialization']}
        if len(instructor_fields) != len(extra_fields):
            raise ValueError('Extra fields do not match the required fields for the Instructor role.')
        user = Instructor(email=self.normalize_email(email=email),first_name=first_name, last_name=last_name,role=role, **instructor_fields)
        user.set_password(password)
        user.save()
        return user

    def create_soldier(self, email, first_name, last_name, password,role, **extra_fields):
        soldier_fields = {k: v for k, v in extra_fields.items() if k in ['unit', 'specialization']}
        if len(soldier_fields) != len(extra_fields):
            raise ValueError('Extra fields do not match the required fields for the Soldier role.')
        user = Soldier(email=self.normalize_email(email=email),first_name=first_name, last_name=last_name,role=role, **soldier_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, last_name, role, password=None):
        # Check for required fields
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, first_name, last_name, role, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
    
    def deactivate(self, uuid):
        # Deactivate user by setting is_active to False
        user = self.get(uuid=uuid)
        user.is_active = False
        user.save()
    

# Custom user model
class User(AbstractBaseUser, PermissionsMixin):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()
    ROLE_CHOICES = (
        ('INSTRUCTOR', 'Instructor'),
        ('SOLDIER', 'Soldier'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,blank=True)

    def __str__(self):
        return self.email

    @property
    def token(self):
        return self._generate_jwt_token()

    def save(self, *args, **kwargs):
        if not self.pk:
            super(User, self).save(*args, **kwargs)
            Settings.objects.create(user=self)
        else:
            super(User, self).save(*args, **kwargs)

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name

    def get_short_name(self):
        return self.first_name

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': str(self.pk),
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token
    
    def fields_dict(self):
        return model_to_dict(
            User,
            fields=[
                field.name
                for field in self._meta.fields
                if field.name in self.__dict__
                and field.name != self._meta.pk.name
            ]
        )

# Instructor model
class Instructor(User):
    experience = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)


# Soldier model
class Soldier(User):
    unit = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)


# Training model
class Training(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT)
    description = models.CharField(max_length=10000, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)

    class TrainingTypes(models.TextChoices):
        ASSAULT = 'Assault', _('Assault')
        SCOUT = 'Scouting', _('Scouting')
        DEMINING = 'Demining', _('Demining')
        MIXED = 'Mixed', _('Mixed')

    type = models.CharField(
        max_length=8,
        choices=TrainingTypes.choices,
        default=TrainingTypes.MIXED
    )
    soldiers = models.ManyToManyField(Soldier)


# Results model
class Results(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.OneToOneField(Training, on_delete=models.CASCADE)
    mines_activated = models.IntegerField(default=0)
    mines_passed = models.IntegerField(default=0)
    mines_defused = models.IntegerField(default=0)
    soldiers_lost = models.IntegerField(default=0)
    time_spent = models.DurationField()


# Task model
class Task(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)

    class TaskTypes(models.TextChoices):
        ASSAULT = 'Assault', _('Assault')
        SCOUT = 'Scouting', _('Scouting')
        DEMINING = 'Demining', _('Demining')

    type = models.CharField(
        max_length=8,
        choices=TaskTypes.choices,
        default=TaskTypes.DEMINING
    )
    description = models.CharField(max_length=10000, blank=True)
    is_completed = models.BooleanField(default=False)


# Settings model
class Settings(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))

    time_zone = models.CharField(max_length=32, choices=TIMEZONES,
                                 default='UTC')

    class Language(models.TextChoices):
        ENGLISH = 'EN', _('English')
        UKRAINIAN = 'UA', _('Ukrainian')

    language = models.CharField(
        max_length=2,
        choices=Language.choices,
        default=Language.ENGLISH
    )

    class MeasurementUnits(models.TextChoices):
        METRIC = 'MT', _('Metric')
        IMPERIAL = 'IM', _('Imperial')

    measurement_units = models.CharField(
        max_length=2,
        choices=MeasurementUnits.choices,
        default=MeasurementUnits.METRIC,
    )


# Mine model
class Mine(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)

    class MineTypes(models.TextChoices):
        TRIPWIRE = 'TW', _('Tripwire mine')
        ANTIPERSONNEL = 'AP', _('Anti-personnel mine')

    type = models.CharField(
        max_length=2,
        choices=MineTypes.choices,
        default=MineTypes.ANTIPERSONNEL,
    )

    range = models.IntegerField(blank=True, null=True)
    is_activated = models.BooleanField(default=False)
    is_defused = models.BooleanField(default=False)


# Map model
class Map(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    training = models.OneToOneField(Training, on_delete=models.CASCADE)
    mines = models.ManyToManyField(Mine, through='MapsMines')
    description = models.CharField(max_length=10000, blank=True)
    start_point = models.PointField(default='POINT(0 0)')
    end_point = models.PointField(null=True, blank=True)


# MapsMines model
class MapsMines(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    mine = models.ForeignKey(Mine, on_delete=models.CASCADE)
    location = models.PointField()
