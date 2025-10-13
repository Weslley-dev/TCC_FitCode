from django.http import JsonResponse
from django.contrib.auth.models import User
from accounts.models import UserProfile
import logging

logger = logging.getLogger(__name__)

def debug_view(request):
    """View de debug para testar conexão com banco"""
    try:
        # Testar conexão 
        user_count = User.objects.count()
        profile_count = UserProfile.objects.count()
        
        return JsonResponse({
            'status': 'success',
            'database': 'connected',
            'user_count': user_count,
            'profile_count': profile_count,
            'debug': True
        })
    except Exception as e:
        logger.error(f"Erro no debug: {e}")
        return JsonResponse({
            'status': 'error',
            'error': str(e),
            'debug': True
        })
