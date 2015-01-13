from django.conf.urls import patterns, include, url
from django.conf import settings
#from django.views.generic import simple
from django.views.generic import DetailView,ListView,UpdateView,CreateView

from santaclara_pages.models import Page
from santaclara_base.decorators import staff_or_404,permission_or_404

urlpatterns =patterns('',
                      ( r'^page/$',ListView.as_view(model=Page,
                                                     context_object_name="page_list")),
                      ( r'^page/(?P<pk>\d+)/?$',
                        permission_or_404("santaclara_pages.view_page",model=Page)(DetailView.as_view(model=Page,
                                                                                                      context_object_name="page"))),
                      ( r'^page/(?P<pk>\d+)-[^/]+/?$',
                        permission_or_404("santaclara_pages.view_page",model=Page)(DetailView.as_view(model=Page,
                                                                                                      context_object_name="page"))),
                      )

