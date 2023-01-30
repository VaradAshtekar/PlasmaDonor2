from django.contrib import admin
from django.urls import path
from donation import views
from django.views.generic import TemplateView
app_name = "donation"

from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name="index"),
    path('faq', views.faqs, name="faqs"),
    path('register', views.signupsys, name = "register"),
    path('compatability', views.compatability, name = "compatability"),
    path('location', views.location, name="location"),
    path('contact', views.contact, name="contact"),
    path('login', views.loginsystem, name = "login"),
    path('donate', views.donor, name="donor")
]
