# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"

from django.shortcuts import get_object_or_404
from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)
from datetime import datetime, time
from datetime import datetime
import schedule
import time
USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

#
# from ..celery123 import *




class MyUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, category, date_of_joining, dirtybit, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )
        user.first_name = first_name
        user.last_name = last_name
        user.category = category
        user.date_of_joining = date_of_joining
        user.dirtybit = dirtybit
        user.set_password(password)
        user.save(using=self._db)

        return user

    # user.password = password # bad - do not do this

    def create_superuser(self, username, email, first_name, last_name, category, date_of_joining, dirtybit,
                         password=None):
        user = self.create_user(
            username, email, first_name, last_name,category, date_of_joining, dirtybit, password=password
        )
        user.first_name = first_name
        user.last_name = last_name
        user.date_of_joining = date_of_joining
        user.dirtybit = dirtybit
        user.is_admin = True
        user.cache_hit = False
        user.email_verified = True
        user.phone_verified = True
        user.is_staff = True
        user.new_user_notify = False
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(
        max_length=300,
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
                           message='Username must be alphanumeric or contain numbers',
                           code='invalid_username'
                           )],
        unique=True
    )
    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name='email address'
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    category = models.CharField(max_length=10, default='creator')
    is_admin = models.BooleanField(default=False)
    cache_hit = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_of_joining = models.DateTimeField(default=datetime.now)
    dirtybit = models.UUIDField(default=uuid.uuid4, unique=True)
    new_user_notify = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'category', 'date_of_joining', 'dirtybit']

    def __str__(self):
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def save(self, *args, **kwargs):
        if self.category == 'Creator':
            super().save(*args, **kwargs)
            obj = MyUser.objects.get(dirtybit=self.dirtybit)
            creator_profile_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            user_connection_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            super().save(*args, **kwargs)
        elif self.category == 'Business':
            super().save(*args, **kwargs)
            obj = MyUser.objects.get(dirtybit=self.dirtybit)
            business_profile_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)

            user_connection_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)

            super().save(*args, **kwargs)
        else:
            pass


class business_profile_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    founded = models.DateField(max_length=255, blank=True, null=True)
    company_category = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    # email = models.EmailField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    overview = models.CharField(max_length=500, blank=True, null=True)
    company_size = models.IntegerField(blank=True, null=True)
    field_of_interest = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    cache_hit = models.BooleanField(default=False, blank=True, null=True)


class creator_profile_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(unique=True, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    artist_category = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    # email = models.EmailField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    cache_hit = models.BooleanField(default=False, blank=True, null=True)


class selected_connections(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    connection_dirtybit = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    provider = models.CharField(blank=False, null=False, max_length=50)
    account_token = models.TextField(blank=True, null=True, max_length=1000)
    access_token = models.TextField(blank=False, null=False, max_length=1000)
    access_token_secret = models.TextField(blank=True, null=True, max_length=1000)
    extra_data = models.TextField(blank=True, null=True, max_length=10000)
    access_expiry = models.DateTimeField(blank=True, null=True)
    long_token = models.CharField(blank=True, null=True, max_length=1000)
    long_expiry = models.DateTimeField(blank=True, null=True)
    account_name = models.CharField(max_length=500, blank=True, null=True)
    account_uid = models.CharField(max_length=500, unique=True, blank=True, null=True)
    selected = models.BooleanField(default=False)
    within_limit = models.BooleanField(default=True)
    auto_sync = models.BooleanField(default=False)
    last_sync = models.DateTimeField(blank=True,null=True)
    def __str__(self):
        return str(self.account_uid)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)




class user_connection_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True, unique=True)
    total_connections = models.IntegerField(default=0)
    total_seleceted_connections = models.IntegerField(default=0)
    fan_count = models.BigIntegerField(default=0)



class facebook_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    fb_id = models.CharField(max_length=1000,blank=True,null=True)
    name = models.CharField(max_length=1000,blank=True,null=True)
    bio = models.CharField(max_length=5000,blank=True,null=True)
    business_id = models.CharField(max_length=1000,blank=True,null=True)
    business_name = models.CharField(max_length=1000,blank=True,null=True)
    category = models.CharField(max_length=1000,blank=True,null=True)
    fan_count = models.BigIntegerField(blank=True,null=True) # int
    featured_video_desc = models.CharField(max_length=1000,blank=True,null=True)
    artists_we_like = models.CharField(max_length=1000,blank=True,null=True)
    connected_instagram_account = models.CharField(max_length=1000,blank=True,null=True)
    cover_source = models.URLField(max_length=2000,blank=True,null=True)#url
    country_page_likes = models.BigIntegerField(blank=True,null=True)#int
    engagement = models.BigIntegerField(blank=True,null=True)#int
    impressum = models.CharField(max_length=1000,blank=True,null=True)
    about = models.CharField(max_length=1000,blank=True,null=True)

    new_like_count = models.BigIntegerField(blank=True,null=True)#int
    overall_star_rating = models.BigIntegerField(blank=True,null=True)#int
    rating_count = models.BigIntegerField(blank=True,null=True) #int
    talking_about_count = models.BigIntegerField(blank=True,null=True) #int
    unread_message_count= models.BigIntegerField(blank=True,null=True) #int
    unread_notif_count= models.BigIntegerField(blank=True,null=True) #int
    unseen_message_count= models.BigIntegerField(blank=True,null=True) #int


    verification_status= models.CharField(max_length=1000,blank=True,null=True)
    website = models.CharField(max_length=1000,blank=True,null=True)
    were_here_count = models.BigIntegerField(blank=True,null=True) #int



class linkedin_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    linkedin_id = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    fan_count = models.BigIntegerField(blank=True, null=True, default=0)  # connections -> currently does not have permission for connections API
    headline = models.CharField(max_length=2000, blank=True, null=True)



class twitter_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    twitter_id = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    screen_name = models.CharField(max_length=1000, blank=True, null=True)
    location = models.CharField(max_length=1000, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    website = models.CharField(max_length=1000, blank=True, null=True)
    fan_count = models.BigIntegerField(blank=True, null=True, default=0)  # followers
    friends_count = models.BigIntegerField(blank=True, null=True, default=0)
    listed_count = models.BigIntegerField(blank=True, null=True, default=0)
    created_at = models.CharField(max_length=1000, blank=True, null=True)
    favourites_count = models.BigIntegerField(blank=True, null=True, default=0)
    verified = models.BooleanField(default=False)
    profile_background_color = models.CharField(max_length=1000, blank=True, null=True)
    profile_background_image_url_https = models.CharField(max_length=1000, blank=True, null=True)
    profile_image_url_https = models.CharField(max_length=1000, blank=True, null=True)
    profile_banner_url = models.CharField(max_length=1000, blank=True, null=True)



class youtube_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    account = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    youtube_id = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    fan_count = models.BigIntegerField(blank=True, null=True, default=0)
    views = models.BigIntegerField(blank=True, null=True, default=0)
    videos_count =models.BigIntegerField(blank=True, null=True, default=0)
    description = models.CharField(max_length=1000, blank=True, null=True)
    link = models.URLField(blank=True,null=True)
    hit = models.BooleanField(default=False)


from datetime import datetime

class notifications(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    sender = models.CharField(max_length=1000, blank=False, null=False)
    message = models.CharField(max_length=1000, blank=False, null=False)
    sender_url = models.URLField(blank=False,null=False)
    notification_type = models.IntegerField(blank=False,null=False)
    datetime = models.DateTimeField(blank=True,null=True)
    read = models.BooleanField(default=False)
    mark_as_read_all = models.BooleanField(default=False)
    read_datetime = models.DateTimeField(blank=True,null=True)



class search(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(default=datetime.now)
    location = models.CharField(max_length=100,blank=False,null=False)
    platform = models.CharField(max_length=100, blank=True, null=True)
    category = models.CharField(max_length=100, blank=False, null=False)
    reach = models.BigIntegerField(blank=True, null=True)
'''


"username","datetime","location","platform","category","reach"


'''