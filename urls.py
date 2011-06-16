from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from chat.main import views
from django.contrib.auth.views import login, logout
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^chat/', include('chat.foo.urls')),
     (r'^$', views.chat_room),
     (r'^refresh/$', views.refresh),
     (r'^reply/$', views.reply),
     (r'^statuses/$', views.msg_session),
     (r'^fav/$', views.favorite),
     (r'^myfav/$', views.myfavorite),
     (r'^search/$', views.search),
     (r'^search/title/(\w+)/$', views.search_title),
     (r'^accounts/login/$', login),
     (r'^accounts/logout/$', logout),
     (r'^accounts/profile/$', direct_to_template,{'template':'profile.html'}),
     (r'^upload/$', views.upload),
     (r'^register/$', views.register),
     (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root':settings.MEDIA_ROOT}),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     (r'^admin/', include(admin.site.urls)),
)
