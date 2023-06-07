from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name="login"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path("logout/", views.logout, name="logout"),
    path("create_event/", views.create_event, name="create_event"),
    path("find_university/", views.find_university, name="find_university"),
    path("find_info/", views.find_info, name="find_info"),
    path("join_event/", views.join_event, name="join_event"),
    path("get_relations/", views.get_relations, name="get_relations")
]