from django.urls import path

from . import views

urlpatterns = [
    path("slides/<int:slide_number>/", views.slide_view, name="slides"),
    path("register/", views.RegisterDriverView.as_view(), name="reg_driver"),
    path("test/", views.test, name="test"),
    path("result/", views.self_result_view, name="user_result"),
    path("result/<int:user_id>/", views.certain_user_result, name="result"),
    path("results/", views.users_result_view, name="results"),
    path("", views.index, name='main'),
    path("logout/", views.logout_view, name="logout_driver")
]
