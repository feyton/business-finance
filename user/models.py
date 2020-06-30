from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, commit=True):
        if not email:
            raise ValueError('User must have an email')
        if not first_name:
            raise ValueError('User must have first name')
        if not last_name:
            raise ValueError('User must have last name')

        user = self.model(
            email=self.normalize_email(email), first_name=first_name, last_name=last_name
        )

        user.set_password(password)
        if commit:
            user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email',
                              max_length=255, unique=True)
    first_name = models.CharField(
        verbose_name='first name', max_length=255, blank=True)
    last_name = models.CharField(
        verbose_name='last name', max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return '%s <%s>' % (self.get_full_name(), self.email)

    def has_perm(self, app_label):
        return True

    def get_short_name(self):
        return '%s' % self.first_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s <Profile>' % self.user.get_full_name()
