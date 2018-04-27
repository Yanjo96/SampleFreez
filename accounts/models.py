# accounts.models.py

from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

class UserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password):
        """
        Creates and saves a User with the given username and password.
        """
        if not email:
            raise ValueError('Users must have an email')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, username, first_name, last_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            username=username,
            password=password,
        )

        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, first_name, last_name, password):
        """
        Creates and saves a superuser with the given username and password.
        """
        user = self.create_user(
            email,
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    THEME_CHOICES = (
        ('cerulean','Cerulean'),
        ('cosmo','Cosmo'),
        ('cyborg','Cyborg'),
        ('darkly','Darkly'),
        ('flatly','Flatly'),
        ('journal','Journal'),
        ('lietra','Lietra'),
        ('lumen','Lumen'),
        ('lux','Lux'),
        ('materia','Matria'),
        ('minty','Minty'),
        ('pulse','Pulse'),
        ('sandstone','Sandstone'),
        ('simplex','Simplex'),
        ('sketchy','Sketchy'),
        ('slate','Slate'),
        ('solar','Solar'),
        ('spacelab','Spacelab'),
        ('superhero','Superhero'),
        ('united','United'),
        ('yeti','Yeti'),
    )

    theme = models.CharField(max_length=50, choices=THEME_CHOICES,  blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    # notice the absence of a "Password field", that's built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','first_name','last_name',] # Username & Password are required by default.

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # All admins have permissions
        return self.is_admin

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    objects = UserManager()
