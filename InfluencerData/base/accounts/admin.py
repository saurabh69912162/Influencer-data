from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import business_profile_data, creator_profile_data
from .forms import UserCreationForm
from .models import *
admin.site.unregister(Group)
# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username','last_login','email','is_admin','first_name','last_name','category','date_of_joining','dirtybit')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','email','last_login','first_name','last_name','category','password','date_of_joining','dirtybit')}),
			('Permissions', {'fields': ('is_admin','email_verified','phone_verified','cache_hit','new_user_notify')})
		)
	search_fields = ('username','email','first_name','last_name','category','date_of_joining','dirtybit')
	ordering = ('username','email','last_name','first_name','last_login',)

	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)


class creator_profile_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','skills','artist_category','location','cache_hit')
	list_filter = ('skills',)

	fieldsets = (
			(None, {'fields': ('username','dirtybit','skills','artist_category','location','cache_hit')}),
			('Description', {'fields': ('description',)})
		)
	search_fields = ('username','dirtybit','skills','artist_category','location','cache_hit')
	ordering = ('username','dirtybit','skills','artist_category','location','cache_hit')

	filter_horizontal = ()


admin.site.register(creator_profile_data, creator_profile_data_admin)



class business_profile_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')
	list_filter = ('company_category','location')

	fieldsets = (
			(None, {'fields': ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')}),
			('Description', {'fields': ('overview',)})
		)
	search_fields = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')
	ordering = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')

	filter_horizontal = ()


admin.site.register(business_profile_data, business_profile_data_admin)

class selected_connections_admin(admin.ModelAdmin):

	list_display = ('username','within_limit','auto_sync','selected','last_sync','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')
	list_filter = ('provider',)

	fieldsets = (
			(None, {'fields': ('username','within_limit','auto_sync','last_sync','selected','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','access_expiry','long_token','long_expiry')}),
			('Description', {'fields': ('extra_data',)})
		)
	search_fields = ('username','selected','account_name','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')
	ordering = ('username','within_limit','selected','auto_sync','last_sync','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')

	filter_horizontal = ()


admin.site.register(selected_connections, selected_connections_admin)

class user_connection_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','total_connections','total_seleceted_connections',)

	filter_horizontal = ()

admin.site.register(user_connection_data, user_connection_data_admin)


class notification_pannel_admin(admin.ModelAdmin):

	list_display = ('username','timestamp','read_hit','mark_as_read_hit','read_hit_time','message','follow_link','u_code')
	filter_horizontal = ()

admin.site.register(notification_pannel, notification_pannel_admin)

class facebook_data_admin(admin.ModelAdmin):


	list_display = ("username","account","fb_id","name","bio","about","category","fan_count","featured_video_desc","artists_we_like","connected_instagram_account","cover_source","country_page_likes","engagement","impressum","new_like_count","overall_star_rating","rating_count","talking_about_count","unread_message_count","unread_notif_count","unseen_message_count","verification_status","website","were_here_count")
	filter_horizontal = ()

admin.site.register(facebook_data, facebook_data_admin)


class linkedin_data_admin(admin.ModelAdmin):


	list_display = ("username","account","linkedin_id","name","headline","fan_count")
	filter_horizontal = ()

admin.site.register(linkedin_data, linkedin_data_admin)



class twitter_data_admin(admin.ModelAdmin):


	list_display = ("username","account","twitter_id","name","description","fan_count",
	"screen_name","location","website","fan_count","friends_count","listed_count",
	"created_at","favourites_count","verified","profile_background_color","profile_background_image_url_https","profile_image_url_https",
	"profile_banner_url")
	filter_horizontal = ()

admin.site.register(twitter_data, twitter_data_admin)


