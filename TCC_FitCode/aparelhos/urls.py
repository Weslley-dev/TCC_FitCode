from django.urls import path
from .views import aparelhos_view, aparelho_delete, aparelho_edit

urlpatterns = [
    path('', aparelhos_view, name='aparelhos_list'),
    path('delete/<int:pk>/', aparelho_delete, name='aparelho_delete'),
    path('edit/<int:pk>/', aparelho_edit, name='aparelho_edit'),
]