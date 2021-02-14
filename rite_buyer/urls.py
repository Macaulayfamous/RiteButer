
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', users_views.register,name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('contact', users_views.contact, name='contact'),
    path('', include('store.urls')),
    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
