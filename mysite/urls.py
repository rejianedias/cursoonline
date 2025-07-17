from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from cursos.views import home
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('accounts/', include('accounts.urls')),
    path('cursos/', include('cursos.urls')),  
    path('quiz/', include('mysite.quiz.urls')),
    path('suporte/', include('suporte.urls')),
    path('blog/', include('blog.urls')),  
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
   
            
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/accounts/login/'
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Para testes



