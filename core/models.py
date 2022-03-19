from django.db import models
from django.contrib.auth.models import AbstractUser , BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=100,  blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return '{}'.format(self.name)


class Salary(models.Model):
    leaves = models.IntegerField(default=1, blank=True, null=True)
    paid_leaves = models.IntegerField(default=1, blank=True, null=True)
    total_days = models.IntegerField(default=1, blank=True, null=True)
    working_days = models.IntegerField(default=1, blank=True, null=True)
    actual_days = models.IntegerField(default=1, blank=True, null=True)
    month = models.DateField(blank=True, null=True)
    employ = models.ForeignKey('core.User', 
                        on_delete=models.CASCADE, null=True, blank=True, related_name='salaries',)

    class Meta:
        verbose_name= "salary"
        verbose_name_plural = "salaries" 

    def __str__(self):
        return '{} - {}'.format(self.employ.name, self.month.strftime('%B, %Y'))