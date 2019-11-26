from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from accounts.views import *
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^profile/$', profile, name='profile'),
    url(r'^register/$', register),
    path('', login_view),
    path('connect/',connect),
    path('insights/',insights),
    path('check-insights/<str:uid>',check_insights),
    path('search/',search),
    path('configure/',configure),
    path('facebook-configure/',facebookconfigure),
    url('^accounts/', include('allauth.urls')),
    path('logout/', logout_view),
    url(r'^password/$', change_password, name='change_password'),
    url(r'^profile/edit$', edit_profile),
    url(r'^profile/details', edit_me),

]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
