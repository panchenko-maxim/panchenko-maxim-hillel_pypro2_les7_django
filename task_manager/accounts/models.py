from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field required')
        if not phone_number:
            raise ValueError('Phone field required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, phone_number, password, **extra_fields)

    def active_users_after_date(self, date):
        return self.filter(is_active=True, date_joined__gte=date)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name='email')
    phone_number = models.CharField(max_length=10, unique=True, verbose_name='phone_number')
    first_name = models.CharField(max_length=30, blank=True, verbose_name='first_name')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='last_name')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='birthday')
    profile_of_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='is_active')
    is_staff = models.BooleanField(default=False, verbose_name='personal')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date of registration')
    preferred_language = models.CharField(max_length=10,
                                          choices=[('ua', 'ukranian'), ('en', 'english')],
                                         default='en',
                                         verbose_name='language')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        permissions = [
            ('can_view_profiles', 'Can watch profiles another users'),
            ('can_edit_profiles', 'Can edit profiles another users'),
        ]

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()


class UserAddress(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='Addresses')
    city = models.CharField(max_length=100, verbose_name='City')
    street = models.CharField(max_length=150, verbose_name='Street')
    postal_code = models.CharField(max_length=10, verbose_name='Index')

    class Meta:
        verbose_name = 'User`s address'
        verbose_name_plural = 'Addresses of users'

    def __str__(self):
        return f'{self.city}, {self.street}'


class UserPayment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Summ')
    payment_date = models.DateTimeField(default=timezone.now, verbose_name='Payment date')
    payment_method = models.CharField(max_length=50, choices=[
        ('card', 'Card'),
        ('cash', 'Cash'),
        ('iban', 'Iban'),
    ], default='card', verbose_name='Payment method')

    def __str__(self):
        return f'{self.user.email} - {self.amount}({self.payment_date})'




