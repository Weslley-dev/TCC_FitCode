from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, CustomPasswordChangeForm
from .models import UserProfile
from aparelhos.models import Feedback
from aparelhos.forms import FeedbackForm

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('login')  # redireciona para login após registro
    else:
        user_form = CustomUserCreationForm()
    return render(request, 'register.html', {'user_form': user_form})

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            # Redirecionar baseado em permissões - apenas WeslleyDev tem acesso admin
            if user.username == 'WeslleyDev' and (user.is_superuser or user.is_staff):
                return redirect('aparelhos_list')  # Admin vai para lista de exercícios com permissões
            else:
                return redirect('user_exercises_list')  # Usuário comum vai para lista sem permissões
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