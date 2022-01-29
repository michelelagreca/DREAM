from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser


# DOC custom user models https://testdriven.io/blog/django-custom-user-model/


# district definition
class District(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# area definition
class Area(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


# auth code definition
class AuthCodeFarmer(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    isValid = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return self.code


class AuthCodeAgronomist(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    area = models.ForeignKey(Area, on_delete=models.PROTECT)
    isValid = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return self.code


class AuthCodePolicyMaker(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT)
    isValid = models.BooleanField(blank=False, default=True)

    def __str__(self):
        return self.code


# Manager for custom user, it is responsible to manage the updates made by code to the user model
# i.e CustomUser.objects.create_user(...)
# The superuser function is the one accessed by the django console

class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('first_name', 'no name')
        other_fields.setdefault('last_name', 'no name')
        other_fields.setdefault('user_name', email)
        other_fields.setdefault('auth_code', 'no code')
        other_fields.setdefault('first_name', 'no name')

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')

        # call to the function below, basically a super user is a normal user
        return self.create_user(email=email, password=password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, auth_code, password, longitude, latitude, **other_fields):

        if not email:
            raise ValueError('You must provide an email address')
        if not user_name:
            raise ValueError('You must provide an user_name')
        if not first_name:
            raise ValueError('You must provide an first name')
        if not last_name:
            raise ValueError('You must provide an last name')
        if not auth_code:
            raise ValueError('You must provide authorization code')
        if not auth_code:
            raise ValueError('You must provide a role')

        # normalization of data before creation
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        print("@@ Create user manager execution...")
        return user


# the mixin binds the django user with our custom one
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    auth_code = models.CharField(max_length=50, blank=False)    # register auth code user for sign up
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)  # if not active cannot receive tokens
    area = models.ForeignKey(Area, on_delete=models.PROTECT, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.PROTECT, null=True)
    role = models.CharField(max_length=20, blank=False, default='no role')
    latitude = models.DecimalField(decimal_places=9, max_digits=13, blank=False)
    longitude = models.DecimalField(decimal_places=9, max_digits=13, blank=False)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'auth_code', 'role', 'latitude', 'user_name', 'longitude']
