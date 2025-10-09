from django.urls import path
from .views import (
    aparelhos_view,
    aparelho_delete,
    aparelho_edit,
    aparelho_create,
    user_exercises_list,
    user_exercise_detail,
    user_feedback,
    user_visualization,
    admin_feedbacks_list,
    admin_reports,
    qr_code_redirect,
    qr_exercise_detail,
    download_qr_pdf
)

urlpatterns = [
    # URLs para administradores
    path('', aparelhos_view, name='aparelhos_list'),
    path('novo/', aparelho_create, name='aparelho_create'),
    path('delete/<int:pk>/', aparelho_delete, name='aparelho_delete'),
    path('edit/<int:pk>/', aparelho_edit, name='aparelho_edit'),
    path('feedbacks/', admin_feedbacks_list, name='admin_feedbacks_list'),
    path('relatorios/', admin_reports, name='admin_reports'),
    
    # URLs para usuários comuns
    path('user/', user_exercises_list, name='user_exercises_list'),
    path('user/exercicio/<int:pk>/', user_exercise_detail, name='user_exercise_detail'),
    path('user/feedback/<int:pk>/', user_feedback, name='user_feedback'),
    path('user/visualizacao/<int:pk>/', user_visualization, name='user_visualization'),
    
    # URLs para fluxo do QR Code
    path('qr/<int:pk>/', qr_code_redirect, name='qr_code_redirect'),
    path('qr/exercicio/<int:pk>/', qr_exercise_detail, name='qr_exercise_detail'),
    
    # URLs para download de PDF
    path('download-qr/<int:pk>/', download_qr_pdf, name='download_qr_pdf'),
]