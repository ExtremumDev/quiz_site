from django.urls import path

from . import views

urlpatterns = [
    path("slides/<int:slide_number>/", views.slide_view, name="slides"),
    path("register/", views.RegisterDriverView.as_view(), name="reg_driver"),
    path("test/", views.test, name="test")
]
