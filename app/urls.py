from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, register_view, logout_view, user_profile, change_password, user_feedbacks, edit_feedback, delete_feedback, logout_view, admin_profile, admin_clients_list, admin_client_detail

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('profile/', user_profile, name='user_profile'),
    path('profile/change-password/', change_password, name='change_password'),
    path('profile/feedbacks/', user_feedbacks, name='user_feedbacks'),
    path('profile/feedbacks/edit/<int:pk>/', edit_feedback, name='edit_feedback'),
    path('profile/feedbacks/delete/<int:pk>/', delete_feedback, name='delete_feedback'),
    path('profile/admin/', admin_profile, name='admin_profile'),
    path('clients/', admin_clients_list, name='admin_clients_list'),
    path('clients/<int:user_id>/', admin_client_detail, name='admin_client_detail'),
    path('aparelhos/', include('aparelhos.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)