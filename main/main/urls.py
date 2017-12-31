# -*- coding: utf-8 -*-
from django.conf.urls import include, url
from django.contrib import admin
from blog.views import Index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', Index.as_view(), name="Index"),
]