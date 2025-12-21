from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path("", views.Hello, name= "Hello"),
    path("register_new_worker/",views.register_new_worker, name = "register_new_worker"),
    path("login/",auth_views.LoginView.as_view(template_name="Users/login.html"),name = "login"),
    path("logout/",auth_views.LogoutView.as_view(),name="logout"),
    path("dashboard/",views.dashboard,name = "dashboard"),
    path("create_ticket/",views.create_ticket,name = "create_ticket"),
    path("my_tickets/",views.my_tickets,name = "my_tickets"),
    path("send_report/<int:ticket_id>/",views.send_report,name = "send_report"),
    path("view_reports/",views.view_reports,name = "view_reports"),
    path("workers/",views.Workers,name = "workers")
]