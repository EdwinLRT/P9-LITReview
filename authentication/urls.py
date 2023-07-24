from django.urls import path
import authentication.views

app_name = "authentication"
urlpatterns = [

    path("signup/", authentication.views.signup_page, name="signup"),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
]
