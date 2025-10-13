from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, CustomPasswordChangeForm
from .models import UserProfile
from aparelhos.models import Feedback
from aparelhos.forms import FeedbackForm
from .decorators import admin_required

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)  # Login automático após registro
            
            # Verificar se veio do fluxo do QR Code
            if request.session.get('qr_redirect', False) and request.session.get('qr_exercise_id'):
                exercise_id = request.session.get('qr_exercise_id')
                return redirect('qr_exercise_detail', pk=exercise_id)
            
            # Redirecionar para lista de exercícios após registro
            return redirect('user_exercises_list')
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    import logging
    logger = logging.getLogger(__name__)
    
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        logger.info(f"Tentativa de login - POST recebido")
        if form.is_valid():
            user = form.get_user()
            logger.info(f"Usuário válido: {user.username}")
            auth_login(request, user)
            
            # Verificar se veio do fluxo do QR Code
            if request.session.get('qr_redirect', False) and request.session.get('qr_exercise_id'):
                exercise_id = request.session.get('qr_exercise_id')
                return redirect('qr_exercise_detail', pk=exercise_id)
            
            # Redirecionar baseado em permissões - superusuários têm acesso admin
            if user.is_superuser or user.is_staff:
                logger.info("Redirecionando para admin")
                return redirect('aparelhos_list')  # Admin vai para lista de exercícios com permissões
            else:
                logger.info("Redirecionando para usuário comum")
                return redirect('user_exercises_list')  # Usuário comum vai para lista sem permissões
        else:
            logger.error(f"Formulário inválido: {form.errors}")
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def user_profile(request):
    """View para editar perfil do usuário"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Verificar se é mudança de senha
        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileForm(instance=profile)
            
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Importante para manter a sessão ativa
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('user_profile')
            else:
                messages.error(request, 'Erro ao alterar senha. Verifique os dados.')
        else:
            # Atualização de perfil normal
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            password_form = CustomPasswordChangeForm(request.user)
            
            # Debug: verificar dados do POST
            print(f"Dados do POST: {request.POST}")
            print(f"Data de nascimento no POST: {request.POST.get('birth_date')}")
            
            # Verificar se deve remover a foto de perfil
            if request.POST.get('remove_profile_picture') == 'true':
                if profile.profile_picture:
                    # Deletar o arquivo físico
                    profile.profile_picture.delete(save=False)
                    # Limpar o campo no banco de dados
                    profile.profile_picture = None
                    profile.save()
                    messages.success(request, 'Foto de perfil removida com sucesso!')
                    return redirect('user_profile')
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('user_profile')
            else:
                # Debug: mostrar erros do formulário
                if not user_form.is_valid():
                    print(f"Erros do user_form: {user_form.errors}")
                if not profile_form.is_valid():
                    print(f"Erros do profile_form: {profile_form.errors}")
                messages.error(request, 'Erro ao atualizar perfil. Verifique os dados.')
    else:
        # Inicializar formulários para GET
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile,
    })

@login_required
def change_password(request):
    """View para alterar senha do usuário"""
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Importante para manter a sessão ativa
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('user_profile')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/change_password.html', {'form': form})

@login_required
def user_feedbacks(request):
    """View para listar feedbacks do usuário"""
    feedbacks = Feedback.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'accounts/user_feedbacks.html', {
        'feedbacks': feedbacks,
    })

@login_required
def edit_feedback(request, pk):
    """View para editar feedback do usuário"""
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Feedback atualizado com sucesso!')
            return redirect('user_feedbacks')
    else:
        form = FeedbackForm(instance=feedback)
    
    return render(request, 'accounts/edit_feedback.html', {
        'form': form,
        'feedback': feedback,
    })

@login_required
def delete_feedback(request, pk):
    """View para excluir feedback do usuário"""
    feedback = get_object_or_404(Feedback, pk=pk, user=request.user)
    
    if request.method == 'POST':
        feedback.delete()
        messages.success(request, 'Feedback excluído com sucesso!')
        return redirect('user_feedbacks')
    
    return render(request, 'accounts/delete_feedback.html', {
        'feedback': feedback,
    })

@admin_required
def admin_profile(request):
    """View para editar perfil do administrador"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        # Verificar se é mudança de senha
        if 'change_password' in request.POST:
            password_form = CustomPasswordChangeForm(request.user, request.POST)
            user_form = UserUpdateForm(instance=request.user)
            profile_form = UserProfileForm(instance=profile)
            
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # Importante para manter a sessão ativa
                messages.success(request, 'Senha alterada com sucesso!')
                return redirect('admin_profile')
            else:
                messages.error(request, 'Erro ao alterar senha. Verifique os dados.')
        else:
            # Atualização de perfil normal
            user_form = UserUpdateForm(request.POST, instance=request.user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
            password_form = CustomPasswordChangeForm(request.user)
            
            # Debug: verificar dados do POST
            print(f"Admin - Dados do POST: {request.POST}")
            print(f"Admin - Data de nascimento no POST: {request.POST.get('birth_date')}")
            
            # Verificar se deve remover a foto de perfil
            if request.POST.get('remove_profile_picture') == 'true':
                if profile.profile_picture:
                    # Deletar o arquivo físico
                    profile.profile_picture.delete(save=False)
                    # Limpar o campo no banco de dados
                    profile.profile_picture = None
                    profile.save()
                    messages.success(request, 'Foto de perfil removida com sucesso!')
                    return redirect('admin_profile')
            
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Perfil atualizado com sucesso!')
                return redirect('admin_profile')
            else:
                # Debug: mostrar erros do formulário
                if not user_form.is_valid():
                    print(f"Admin - Erros do user_form: {user_form.errors}")
                if not profile_form.is_valid():
                    print(f"Admin - Erros do profile_form: {profile_form.errors}")
                messages.error(request, 'Erro ao atualizar perfil. Verifique os dados.')
    else:
        # Inicializar formulários para GET
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'accounts/admin_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'profile': profile,
    })

@admin_required
def admin_clients_list(request):
    """View para listar todos os clientes/usuários cadastrados"""
    # Buscar todos os usuários com seus perfis
    users = User.objects.select_related('profile').all().order_by('first_name', 'last_name', 'username')
    
    # Filtro de busca
    search_query = request.GET.get('q', '')
    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Adicionar informações do perfil para cada usuário
    clients_data = []
    for user in users:
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            profile = None
        
        clients_data.append({
            'user': user,
            'profile': profile,
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'email': user.email,
            'phone': profile.phone if profile else '',
            'birth_date': profile.birth_date if profile else None,
            'profile_picture': profile.profile_picture if profile else None,
            'bio': profile.bio if profile else '',
        })
    
    return render(request, 'accounts/admin_clients_list.html', {
        'clients': clients_data,
        'search_query': search_query,
        'total_clients': len(clients_data),
    })

@admin_required
def admin_client_detail(request, user_id):
    """View para visualizar detalhes de um cliente específico"""
    user = get_object_or_404(User, id=user_id)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    
    client_data = {
        'user': user,
        'profile': profile,
        'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
        'email': user.email,
        'phone': profile.phone if profile else '',
        'birth_date': profile.birth_date if profile else None,
        'profile_picture': profile.profile_picture if profile else None,
        'bio': profile.bio if profile else '',
        'date_joined': user.date_joined,
        'last_login': user.last_login,
    }
    
    return render(request, 'accounts/admin_client_detail.html', {
        'client': client_data,
    })