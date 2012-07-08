from django.conf.urls import patterns, include, url
import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'grs.views.home', name='home'),
    # url(r'^grs/', include('grs.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^$', 'gift.views.index'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', 'gift.views.fb'),
    url(r'', include('social_auth.urls')),
    url(r'^logged/$', 'gift.views.logged'),
	url(r'^gift/search/$', 'gift.views.search'),
    url(r'^logout/$', 'gift.views.logout'),
    url(r'^friends/$', 'gift.views.friends'),
    url(r'^friends_likes/(?P<id>\d+)/$', 'gift.views.friendsLikes'),
    url(r'^recommendations/(?P<id>\d+)/$', 'gift.views.recommendations'),
    url(r'^gift/$', 'gift.views.index'),
    url(r'^gift/templates$', 'gift.views.templates'),

)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)
