"""
URL configuration for LITReview project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import authentication.views
import appreview.views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', authentication.views.login_page, name='login'),
    path('logout/', authentication.views.logout_page, name='logout'),
    path('signup/', authentication.views.signup_page, name='signup'),
    path('photo/upload/', appreview.views.photo_upload, name='upload_photo'),
    path('home/', appreview.views.home, name='home'),
    path('product/create/', appreview.views.product_and_photo_upload, name='create_product'),
    path('product/<int:product_id>/', appreview.views.view_product, name='view_product'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)