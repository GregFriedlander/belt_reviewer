from django.conf.urls import url 
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^delete/(?P<book_id>\d+)$', views.delete),
    url(r'^books$', views.books),
    url(r'^books/add$', views.add),
    url(r'^processreview$', views.processreview),
    url(r'^addreview/(?P<book_id>\d+)$', views.addreview),
    url(r'^books/(?P<book_id>\d+)$', views.bookview),
    url(r'^users/(?P<user_id>\d+)$', views.userdisplay),
]