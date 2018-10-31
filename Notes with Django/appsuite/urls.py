from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'appsuite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Uncomment the next line to enable the admin.
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^notes/', include('notes.urls')),
)