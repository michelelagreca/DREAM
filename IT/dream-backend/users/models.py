from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser


# DOC custom user models https://testdriven.io/blog/django-custom-user-model/

# Manager for custom user
class CustomAccountManager(BaseUserManager):

    def create_superuser(self, email, user_name, last_name, auth_code, first_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True.')
        # TODO fix super user creation
        # call to the function below, basically a super user is a normal user
        return self.create_user(email, user_name,  first_name, last_name, auth_code, password, **other_fields)

    def create_user(self, email, user_name, first_name, last_name, auth_code, password, **other_fields):
        # TODO check this checks
        if not email:
            raise ValueError('You must provide an email address')
        if not first_name:
            raise ValueError('You must provide an first name')
        if not last_name:
            raise ValueError('You must provide an last name')
        if not auth_code:
            raise ValueError('You must provide authcode')

        # normalization of data before creation
        # TODO check that all the needed dat ais managed and associate zone and district
        # TODO manage the reactivation of a policymaker account
        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


# the mixin binds the django user with our custom one
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email address', unique=True)
    user_name = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    auth_code = models.CharField(max_length=50, blank=False)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    zone = models.CharField(max_length=150, blank=False)
    district = models.CharField(max_length=150, blank=False, default='no district')
    role = models.CharField(max_length=20, blank=False, default='no role')

    objects = CustomAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'auth_code', 'role', 'user_name']

    def __str__(self):
        return self.user_name


# district definition
class District(models.Model):
    name = models.CharField(max_length=50)


# zone definition
class Zone(models.Model):
    name = models.CharField(max_length=50)
    district = models.ForeignKey(District, on_delete=models.PROTECT)


# auth code definition
class AuthCodeFarmer(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    # objects = models.Manager()

    def __str__(self):
        return self.code


class AuthCodeAgronomist(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

    def __str__(self):
        return self.code


class AuthCodePolicyMaker(models.Model):
    code = models.CharField(max_length=30, primary_key=True)
    first_name = models.CharField(max_length=150, blank=False)
    last_name = models.CharField(max_length=150, blank=False)
    district = models.ForeignKey(District, on_delete=models.PROTECT)

    def __str__(self):
        return self.code
