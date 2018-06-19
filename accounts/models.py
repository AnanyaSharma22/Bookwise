'''
Accounts Models
'''
import itertools
import random
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser,
                                        PermissionsMixin,
                                        BaseUserManager)
from bookstore.core.email import Email
from bookstore.core.string import Hash
from . import message
from django.utils import timezone

class UserManager(BaseUserManager):
    '''
    User Custom Manager
    '''

    def create_user(self, email=None, password=None):
        '''
        Create User
        '''
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email))
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        '''
        Create Superuser
        '''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''
    If no need to use UserGroups/Permissions then remove PermissionsMixin
    '''
    email = models.EmailField('Email Address', unique=True)
    fb_id = models.CharField(max_length=1000, null=True, blank=True)
    firstname = models.CharField('First Name', max_length=20, db_index=True)
    lastname = models.CharField('Last Name', max_length=20, db_index=True)
    mobile_number = models.CharField(
        'Mobile Number', max_length=20, null=True, blank=True)
    image = models.ImageField(null=True, blank= True, upload_to='user_image/')
    address = models.ForeignKey('Address', max_length=100, blank=True, null=True, related_name='add')
    is_staff = models.BooleanField('Staff member', default=False)
    is_active = models.BooleanField('Active', default=False)
    is_superuser = models.BooleanField('Is a Super user', default=False)
    create_date = models.DateTimeField('Joined Time', auto_now_add=True)
    modify_date = models.DateTimeField(auto_now=True)
    is_app_user = models.BooleanField('App User', default=False)
    objects = UserManager()


    def get_full_name(self):
        return '{0} {1}'.format(self.name, self.name)

    def __str__(self):
        return self.email

    def get_short_name(self):
        return '{0}'.format(self.firstname, )

    USERNAME_FIELD = 'email'

    class Meta:
        ''' User Class Meta '''
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        app_label = 'accounts'


class UserSecurityToken(models.Model):
    '''
    User Security Token
    '''
    FORGOT_PASSWORD = 1
    ACCOUNT_ACTIVATION_TOKEN = 2
    OTP_MOBILE = 3
    OTP_REGISTER_VERIFY_TOKEN = 4
    TOKEN_TYPE_CHOICE = (
        (FORGOT_PASSWORD, 'Forgotten Password'),
        (ACCOUNT_ACTIVATION_TOKEN, 'Account Activation Link'),
        (OTP_MOBILE, 'One Time Password'),
        (OTP_REGISTER_VERIFY_TOKEN, 'OTP Verify Token')
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, related_name='tokens')
    token = models.CharField(max_length=150)
    token_type = models.SmallIntegerField(choices=TOKEN_TYPE_CHOICE)
    extras = models.CharField(max_length=200, null=True, blank=True)
    expire_date = models.DateTimeField()

    def __str__(self):
        if self.user:
            return self.user.email
        return self.extras

    @property
    def encoded_token(self):
        ''' Encoded token '''
        return Hash.encrypt_string(self.token).decode('utf-8')

    @staticmethod
    def create_otp(expiry_date, token_type, user=None, extras=None):
        '''
        Create Otp
        '''
        token = random.randint(1111, 9999)
        data = {
            'user': user,
            'token': '{0:04d}'.format(token),
            'token_type': token_type,
            'expire_date': expiry_date,
            'extras': extras
        }

        return UserSecurityToken.objects.create(**data)

    @staticmethod
    def create_forgot_password_token(user):
        '''
        create Forgot Password token
        '''
        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        UserSecurityToken.objects.filter(user=user,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.FORGOT_PASSWORD).update(expire_date=timezone.now())
        return UserSecurityToken.create_otp(expire, UserSecurityToken.FORGOT_PASSWORD, user=user)

    @staticmethod
    def create_activation_token(email):
        '''
        creating activation token
        '''
        expire = timezone.now() + timezone.timedelta(**settings.ACCOUNT_VERIFY_TOKEN_EXPIRE_IN)
        UserSecurityToken.objects.filter(extras=email,
                                         expire_date__gte=timezone.now(),
                                         token_type=UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN).update(expire_date=timezone.now())
        token = UserSecurityToken.create_otp(
            expire, UserSecurityToken.ACCOUNT_ACTIVATION_TOKEN, extras=email)
        return token

    @staticmethod
    def get_token_by_encoded_token(encoded_token, search_data=None):
        '''
        Token By Encoded Token
        '''
        search_data = search_data if search_data else {}
        encoded_token = Hash.decrypt_string(encoded_token.encode('utf-8'))
        search_data.update({
            'token': encoded_token.decode('utf-8')
        })
        return UserSecurityToken.objects.select_related('user').get(**search_data)

    def send_verify_token_email(self, request):
        ''' Verify TOken '''
        Email(self.extras,
              message.SUBJECT_ACCOUNT_ACTIVATION_TOKEN).message_from_template('accounts/email/account_activation_email.html',
                                                                              {'token': self.token}, request).send()
        return self

    def send_forgot_password_email(self, request):
        '''  Forgot Password Email '''
        Email(self.user.email,
              message.SUBJECT_FORGOT_PASSWORD).message_from_template('accounts/email/forgot_password_email.html',
                                                                     {'token': self.token,
                                                                      'firstname': self.user.firstname,
                                                                      'lastname': self.user.lastname}, request).send()
        return self
   
class ContactUs(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    email = models.EmailField('Email Address')
    message = models.TextField(max_length=500)
    def __str__(self):
        return self.first_name
    class Meta:
        ''' ContactUs Class Meta '''
        verbose_name = 'ContactUs'
        verbose_name_plural = 'ContactUs'
        app_label = 'accounts'

    @classmethod
    def contact_us_email(cls, request, instance):
        '''
        sends email to Admin.
        '''
        admin_user = get_user_model().objects.filter(is_superuser=True).first()
        to_email = settings.DEFAULT_CONTACT_US_EMAIL
        message = instance.message
        email = Email(to_email, subject=instance.email,html_message=instance.message)
        # context = {
        #     'first_name': instance.first_name,
        #     'last_name': instance.last_name,
        #     'email': instance.email,
        #     # 'message': instance.message,
        #     'admin_firstname': admin_user.firstname,
        #     'admin_lastname': admin_user.lastname
        # }
        # email.message_from_template(
        #     'templates/layouts/contact.html', context, request)
        email.send()# class SocialProfile(models.Model):
    
class Address(models.Model):
    user = models.OneToOneField(User, related_name='user')
    house_no = models.CharField('house-no', max_length=100)
    landmark = models.CharField('landmark', max_length=50, default='')
    pincode = models.CharField('pincode', max_length=7)
    city = models.CharField('city', max_length=70)
    state = models.CharField('state', max_length=70)
    country = models.CharField('country', max_length=70)

    def __str__(self):
        return self.house_no

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Address'

