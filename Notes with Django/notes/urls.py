from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from models import NoteResource

v1_api = Api(api_name='v1')
v1_api.register(NoteResource())

from notes.views import index,example,dashboard,dologout

urlpatterns = patterns('',
    # Examples:s
    # url(r'^$', 'appsuite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Uncomment the next line to enable the admin.
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^index/',index,name="index"),
    url(r'^example/',example,name="example"),
    url(r'^dashboard/',dashboard,name="dashboard"),
    url(r'^logout/',dologout,name="logout"),
    url(r'^api/', include(v1_api.urls)),

)
