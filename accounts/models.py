from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.base_user import BaseUserManager



class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, role, password=None):
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, username=username, role=role)
        user.set_password(password)
        user.is_active = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None):
        if email:
            email = self.normalize_email(email)

        user = self.model(email=email, username=username)
        user.set_password(password)
        user.role = 'superuser'
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user





class Account(AbstractUser):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('employee', 'Employee'),
        ('customer', 'Customer')
    )
    role = models.CharField(max_length= 20, choices=ROLE_CHOICES)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField()
    date_joined = models.DateField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    required_field = ['email']

    objects = CustomUserManager()

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True
