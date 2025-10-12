from .models import UserProfile

def user_profile(request):
    """Context processor para disponibilizar o perfil do usuário em todos os templates"""
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            # Não criar perfil automaticamente no context processor
            # Deixar para ser criado nas views específicas
            profile = None
        return {'user_profile': profile}
    return {'user_profile': None}
