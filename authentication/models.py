from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class AccountManager(BaseUserManager):
    def create_user(self, email, login, phone, password=None):
        if not email:
            raise ValueError("The Email field must be set")
        user = self.model(email=email, login=login, phone=phone)
        user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, login, phone, password=None):
        user = self.create_user(email, login, phone, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    login = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, unique=True)
    phone = models.CharField(max_length=200)
    date_creation = models.DateTimeField("date creation", auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['login']

    objects = AccountManager()

    def __str__(self):
        return self.email
