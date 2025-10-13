from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import admin_required, user_required
from .models import Aparelho, Grupo_muscular, Feedback, Visualizacao
from .forms import AparelhoForm, FeedbackForm
from django.urls import reverse
from django.db.models import Count, Avg
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.conf import settings
from django.http import HttpResponse
from django.utils import timezone
from io import BytesIO


@admin_required
def aparelhos_view(request):
    query = request.GET.get('q', '')
    grupo_filter = request.GET.get('grupo', '')
    
    aparelhos = Aparelho.objects.all()
    
    if query:
        aparelhos = aparelhos.filter(exercise_name__icontains=query)
    
    if grupo_filter:
        aparelhos = aparelhos.filter(grupo_muscular_id=grupo_filter)
    
    grupos = Grupo_muscular.objects.all()
    return render(request, 'aparelhos/aparelhos_list.html', {
        'aparelhos': aparelhos,
        'grupos': grupos,
        'request': request,
        'grupo_selecionado': grupo_filter,
    })

@admin_required
def aparelho_delete(request, pk):
    aparelho = get_object_or_404(Aparelho, pk=pk)
    if request.method == 'POST':
        aparelho.delete()
        return redirect('aparelhos_list')
    return render(request, 'aparelhos/aparelhos_confirmacao.html', {'aparelho': aparelho})

@admin_required
def aparelho_edit(request, pk):
    aparelho = get_object_or_404(Aparelho, pk=pk)
    if request.method == 'POST':
        form = AparelhoForm(request.POST, request.FILES, instance=aparelho)
        if form.is_valid():
            form.save()
            return redirect('aparelhos_list')
    else:
        form = AparelhoForm(instance=aparelho)
    return render(request, 'aparelhos/aparelho_edit.html', {'form': form, 'aparelho': aparelho})

@admin_required
def aparelho_create(request):
    if request.method == 'POST':
        form = AparelhoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('aparelhos_list')
    else:
        form = AparelhoForm()
    return render(request, 'aparelhos/aparelho_create.html', {'form': form})

# Views para usuários comuns
@user_required
def user_exercises_list(request):
    """
    View para usuários comuns visualizarem exercícios
    """
    query = request.GET.get('q', '')
    grupo_filter = request.GET.get('grupo', '')
    
    aparelhos = Aparelho.objects.all()
    
    if query:
        aparelhos = aparelhos.filter(exercise_name__icontains=query)
    
    if grupo_filter:
        aparelhos = aparelhos.filter(grupo_muscular_id=grupo_filter)
    
    grupos = Grupo_muscular.objects.all()
    
    return render(request, 'aparelhos/user_exercises_list.html', {
        'aparelhos': aparelhos,
        'grupos': grupos,
        'query': query,
        'grupo_filter': grupo_filter,
    })

@user_required
def user_exercise_detail(request, pk):
    """Detalhes do exercício para usuários comuns"""
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    # Verificar se o usuário já deu feedback
    user_feedback = Feedback.objects.filter(user=request.user, aparelho=aparelho).first()
    
    # Estatísticas do exercício (usando Sum para contar visualizações corretamente)
    from django.db.models import Sum
    total_visualizacoes = Visualizacao.objects.filter(aparelho=aparelho).aggregate(
        total=Sum('count')
    )['total'] or 0
    total_feedbacks = Feedback.objects.filter(aparelho=aparelho).count()
    media_rating = Feedback.objects.filter(aparelho=aparelho).aggregate(Avg('rating'))['rating__avg'] or 0
    
    return render(request, 'aparelhos/user_exercise_detail.html', {
        'aparelho': aparelho,
        'user_feedback': user_feedback,
        'total_visualizacoes': total_visualizacoes,
        'total_feedbacks': total_feedbacks,
        'media_rating': round(media_rating, 1),
    })

@user_required
def user_feedback(request, pk):
    """Página para o usuário dar feedback"""
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    # Verificar se já existe feedback
    existing_feedback = Feedback.objects.filter(user=request.user, aparelho=aparelho).first()
    
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            if existing_feedback:
                # Atualizar feedback existente
                existing_feedback.rating = form.cleaned_data['rating']
                existing_feedback.comment = form.cleaned_data['comment']
                existing_feedback.save()
                messages.success(request, 'Feedback atualizado com sucesso!')
                return redirect('user_feedbacks')
            else:
                # Criar novo feedback
                form.instance.user = request.user
                form.instance.aparelho = aparelho
                form.save()
                messages.success(request, 'Feedback enviado com sucesso!')
                return redirect('user_exercises_list')
    else:
        if existing_feedback:
            form = FeedbackForm(instance=existing_feedback)
        else:
            form = FeedbackForm()
    
    return render(request, 'aparelhos/user_feedback.html', {
        'form': form,
        'aparelho': aparelho,
        'existing_feedback': existing_feedback,
    })


@user_required
@csrf_exempt
@require_POST
def user_visualization(request, pk):
    """View para contar visualização de um exercício"""
    from django.db import transaction
    from django.utils import timezone
    
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    # Usar transação atômica para evitar race conditions
    with transaction.atomic():
        # Criar ou buscar visualização existente
        visualizacao, created = Visualizacao.objects.get_or_create(
            aparelho=aparelho,
            user=request.user,
            defaults={
                'count': 1,
                'last_clicked': timezone.now()
            }
        )
        
        # Se já existe, verificar cooldown
        if not created:
            if not visualizacao.can_click_again():
                remaining_time = visualizacao.get_remaining_cooldown()
                minutes = remaining_time // 60
                seconds = remaining_time % 60
                
                return JsonResponse({
                    'success': False,
                    'message': f'Aguarde {minutes:02d}:{seconds:02d} para contar visualização novamente!',
                    'cooldown': remaining_time
                })
            
            # Incrementar contador e atualizar timestamp
            visualizacao.count += 1
            visualizacao.last_clicked = timezone.now()
            visualizacao.save()
    
    return JsonResponse({
        'success': True,
        'message': 'Visualização contada com sucesso!',
        'count': visualizacao.count
    })

@admin_required
def admin_reports(request):
    """Tela de relatórios para o administrador"""
    from django.db.models import Count, Avg, Sum
    
    # Buscar exercícios com estatísticas
    exercicios_stats = Aparelho.objects.annotate(
        total_visualizacoes=Sum('visualizacoes__count'),
        media_rating=Avg('feedbacks__rating'),
        total_feedbacks=Count('feedbacks')
    ).filter(total_visualizacoes__gt=0).order_by('-total_visualizacoes')
    
    # Preparar dados para o template
    exercicios_ranking = []
    for i, aparelho in enumerate(exercicios_stats, 1):
        exercicios_ranking.append({
            'posicao': i,
            'nome': aparelho.exercise_name,
            'visualizacoes': aparelho.total_visualizacoes or 0,
            'nota': round(aparelho.media_rating or 0, 1),
            'total_feedbacks': aparelho.total_feedbacks or 0
        })
    
    context = {
        'exercicios_ranking': exercicios_ranking,
        'total_exercicios': exercicios_stats.count(),
        'total_visualizacoes_geral': sum(item['visualizacoes'] for item in exercicios_ranking)
    }
    
    return render(request, 'aparelhos/admin_reports.html', context)

@admin_required
def admin_feedbacks_list(request):
    """Lista todos os feedbacks para o administrador"""
    from django.db.models import Q
    
    feedbacks = Feedback.objects.select_related('user', 'aparelho').all().order_by('-created_at')
    
    # Estatísticas gerais
    total_feedbacks = feedbacks.count()
    avg_rating = feedbacks.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
    
    # Filtros
    rating_filter = request.GET.get('rating', '')
    search_query = request.GET.get('q', '')
    
    if rating_filter:
        feedbacks = feedbacks.filter(rating=rating_filter)
    
    if search_query:
        feedbacks = feedbacks.filter(
            Q(user__username__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(aparelho__exercise_name__icontains=search_query) |
            Q(comment__icontains=search_query)
        )
    
    context = {
        'feedbacks': feedbacks,
        'total_feedbacks': total_feedbacks,
        'avg_rating': round(avg_rating, 1),
        'rating_filter': rating_filter,
        'search_query': search_query,
    }
    
    return render(request, 'aparelhos/admin_feedbacks_list.html', context)

# Views para fluxo do QR Code
def qr_code_redirect(request, pk):
    """
    View para redirecionar QR Code para login
    Salva o ID do exercício na sessão para redirecionamento após login
    """
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    # Se usuário já está logado, redireciona direto para o exercício
    if request.user.is_authenticated:
        return redirect('qr_exercise_detail', pk=pk)
    
    # Salva o ID do exercício na sessão para redirecionamento após login
    request.session['qr_exercise_id'] = pk
    request.session['qr_redirect'] = True
    
    # Adicionar mensagem informativa
    from django.contrib import messages
    messages.info(request, f'Faça login para acessar o exercício: {aparelho.exercise_name}')
    
    # Redireciona para login
    return redirect('login')

@user_required
def qr_exercise_detail(request, pk):
    """
    View para exibir exercício específico do QR Code
    Acessível após login via QR Code
    """
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    # Verifica se o usuário veio do fluxo do QR Code
    is_qr_flow = request.session.get('qr_redirect', False)
    qr_exercise_id = request.session.get('qr_exercise_id')
    
    # Se veio do QR code, limpa as flags da sessão
    if is_qr_flow and qr_exercise_id == pk:
        request.session.pop('qr_redirect', None)
        request.session.pop('qr_exercise_id', None)
    
    # Busca feedback do usuário para este exercício
    user_feedback = None
    if request.user.is_authenticated:
        try:
            user_feedback = Feedback.objects.get(user=request.user, aparelho=aparelho)
        except Feedback.DoesNotExist:
            user_feedback = None
    
    # Estatísticas do exercício
    from django.db.models import Sum
    total_visualizacoes = Visualizacao.objects.filter(aparelho=aparelho).aggregate(
        total=Sum('count')
    )['total'] or 0
    
    total_feedbacks = Feedback.objects.filter(aparelho=aparelho).count()
    
    avg_rating = Feedback.objects.filter(aparelho=aparelho).aggregate(
        avg=Avg('rating')
    )['avg'] or 0
    
    context = {
        'aparelho': aparelho,
        'user_feedback': user_feedback,
        'total_visualizacoes': total_visualizacoes,
        'total_feedbacks': total_feedbacks,
        'media_rating': round(avg_rating, 1) if avg_rating else 0,
        'is_qr_flow': is_qr_flow,  # Flag para identificar que veio do QR Code
    }
    
    return render(request, 'aparelhos/qr_exercise_detail.html', context)

@admin_required
def download_qr_pdf(request, pk):
    """
    View para baixar QR Code em PDF
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.units import mm
        from reportlab.pdfgen import canvas
        from reportlab.lib.utils import ImageReader
    except ImportError:
        messages.error(request, 'Biblioteca ReportLab não encontrada. Entre em contato com o administrador.')
        return redirect('aparelhos_list')
    
    aparelho = get_object_or_404(Aparelho, pk=pk)
    
    if not aparelho.qr_code:
        messages.error(request, 'QR Code não encontrado para este exercício.')
        return redirect('aparelhos_list')
    
    # Criar buffer para o PDF
    buffer = BytesIO()
    
    # Criar canvas do PDF
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Configurações
    qr_size = 80 * mm  # Tamanho do QR Code
    margin = 20 * mm   # Margem
    
    # Título
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin, height - margin - 20, "QR Code do Exercício")
    
    # Nome do exercício
    c.setFont("Helvetica", 14)
    exercise_name = aparelho.exercise_name or "Sem nome"
    c.drawString(margin, height - margin - 50, f"Exercício: {exercise_name}")
    
    # Grupo muscular
    if aparelho.grupo_muscular:
        c.setFont("Helvetica", 12)
        c.drawString(margin, height - margin - 70, f"Grupo Muscular: {aparelho.grupo_muscular.name}")
    
    # Centralizar QR Code na página
    qr_x = (width - qr_size) / 2
    qr_y = (height - qr_size) / 2 - 50
    
    # Adicionar QR Code
    try:
        qr_image = ImageReader(aparelho.qr_code.path)
        c.drawImage(qr_image, qr_x, qr_y, width=qr_size, height=qr_size)
    except Exception as e:
        # Se houver erro ao carregar a imagem, desenhar um retângulo
        c.setStrokeColorRGB(0.8, 0.8, 0.8)
        c.setFillColorRGB(0.9, 0.9, 0.9)
        c.rect(qr_x, qr_y, qr_size, qr_size, fill=1, stroke=1)
        c.setFillColorRGB(0, 0, 0)
        c.setFont("Helvetica", 10)
        c.drawString(qr_x + 10, qr_y + qr_size/2, "QR Code não disponível")
    
    # Instruções de uso
    c.setFont("Helvetica", 10)
    instructions_y = qr_y - 30
    c.drawString(margin, instructions_y, "Instruções:")
    c.drawString(margin, instructions_y - 15, "1. Escaneie o QR Code com seu celular")
    c.drawString(margin, instructions_y - 30, "2. Faça login no sistema")
    c.drawString(margin, instructions_y - 45, "3. Acesse as informações do exercício")
    
    # Rodapé
    c.setFont("Helvetica", 8)
    c.drawString(margin, margin, f"Gerado em: {timezone.now().strftime('%d/%m/%Y às %H:%M')}")
    c.drawString(margin, margin - 10, "Sistema FitCode - QR Code para Exercícios")
    
    # Finalizar PDF
    c.showPage()
    c.save()
    
    # Preparar resposta
    buffer.seek(0)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="qr_code_{aparelho.id}_{exercise_name.replace(" ", "_")}.pdf"'
    
    return response