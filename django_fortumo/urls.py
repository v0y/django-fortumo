from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(
        r'^payment_processor$',
        'fortumo.views.payment_processor',
        name='payment_processor',
    ),

    url(r'^admin/', include(admin.site.urls)),
]
