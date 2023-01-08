from django.urls import path
from customer import views

urlpatterns=[
    path("register", views.SignUpView.as_view(), name="register"),
    path("customers/login", views.SigninView.as_view(),name="signin" ),
    path("customers/home", views.HomeView.as_view(), name="user-home")
    
]