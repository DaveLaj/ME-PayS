from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save  
from django.contrib.auth.models import Group
from django_cryptography.fields import encrypt
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.

        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
       
        allgroup = []
        groups = Group.objects.all
        for group in groups():
            allgroup.append(group)
        user = self.create_user(email, password, **extra_fields)
        user.groups.set(allgroup)
        return user
    
    def create_enduser(self, email, password=None, **extra_fields):
        group = Group.objects.get(name='enduser')
        user = self.create_user(email, password, **extra_fields)
        user.groups.set([group])
        return user
    
    def create_pos(self, email, password=None, **extra_fields):
        group = Group.objects.get(name='pos')
        user = self.create_user(email, password, **extra_fields)
        user.groups.set([group])
        return user
    
    def create_cashier(self, email, password=None, **extra_fields):
        group = Group.objects.get(name='cashier')
        user = self.create_user(email, password, **extra_fields)
        user.groups.set([group])
        return user
    


    
    
    
    # def create_cashier(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('role', Role.CASHIER)
    #     return self.create_user(email, password, **extra_fields)
    
    # def get_cashier(self):
    #     return self.get_queryset().filter(role=Role.CASHIER)
    
    # def create_pos(self, email, password=None, **extra_fields):
    #     extra_fields.setdefault('role', Role.POS)
    #     return self.create_user(email, password, **extra_fields)
    
    # def get_pos(self):
    #     return self.get_queryset().filter(role=Role.POS)
    
       

class CustomUser(AbstractBaseUser, PermissionsMixin):
    
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    


class EndUser(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='enduser')
    rfid_code = encrypt(models.CharField(max_length=100, blank=True, null=True))
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    contact_number = models.BigIntegerField()
    school_id = models.IntegerField()
    credit_balance = models.FloatField(default=0)
    loan_balance = models.FloatField(default=0)



class Cashier(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='cashier')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=60)
    contact_number = models.CharField(max_length=10)

    


class POS(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=30, blank=True)
    contact_number = models.BigIntegerField()
    location = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

class Admin(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    contact_number = models.BigIntegerField()




# technique to create placeholder on creation of CustomUser instance
# @receiver(post_save, sender=EndUser)
# def create_enduser_profile(sender, instance, created, **kwargs):
#     if created and instance.role == "ENDUSER":
#         EndUser.objects.create(user=instance)

