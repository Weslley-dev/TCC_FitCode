from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages

def admin_required(view_func):
    """
    Decorator que verifica se o usuário é o administrador autorizado (WeslleyDev)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        if request.user.username != 'WeslleyDev' or not (request.user.is_superuser or request.user.is_staff):
            messages.error(request, 'Você não tem permissão para acessar esta área.')
            return redirect('user_exercises_list')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def user_required(view_func):
    """
    Decorator que verifica se o usuário está logado (usuários comuns)
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')
        
        # Se for o admin, redireciona para área administrativa
        if request.user.username == 'WeslleyDev' and (request.user.is_superuser or request.user.is_staff):
            return redirect('aparelhos_list')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view
