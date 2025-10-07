from django.shortcuts import render, get_object_or_404, redirect
from .models import Aparelho, Grupo_muscular
from django.urls import reverse
from django import forms

def aparelhos_view(request):
    query = request.GET.get('q', '')
    if query:
        aparelhos = Aparelho.objects.filter(exercise_name__icontains=query)
    else:
        aparelhos = Aparelho.objects.all()
    grupos = Grupo_muscular.objects.all()
    return render(request, 'aparelhos/aparelhos_list.html', {
        'aparelhos': aparelhos,
        'grupos': grupos,
        'request': request,
    })

def aparelho_delete(request, pk):
    aparelho = get_object_or_404(Aparelho, pk=pk)
    aparelho.delete()
    return redirect(reverse('aparelhos_list'))

class AparelhoForm(forms.ModelForm):
    class Meta:
        model = Aparelho
        fields = ['exercise_name', 'instructions', 'grupo_muscular', 'image', 'video']

def aparelho_edit(request, pk):
    aparelho = get_object_or_404(Aparelho, pk=pk)
    if request.method == 'POST':
        form = AparelhoForm(request.POST, request.FILES, instance=aparelho)
        if form.is_valid():
            form.save()
            return redirect('aparelhos_list')
    else:
        form = AparelhoForm(instance=aparelho)
    return render(request, 'aparelhos/aparelho_edit.html', {'form': form})