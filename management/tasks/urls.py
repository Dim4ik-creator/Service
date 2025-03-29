from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path("login/", views.login_view, name="login"),
    path("register/",views.register, name="register"),
    path("logout",views.logout_view, name="logout"),
    path('board/', views.board_view, name='board'),
    path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    path('update-status/<int:task_id>/', views.update_status, name='update_status'),
]
