from django import forms
from .models import Aparelho, Feedback

class AparelhoForm(forms.ModelForm):
    class Meta:
        model = Aparelho
        fields = ['exercise_name', 'grupo_muscular', 'video', 'instructions']
        widgets = {
            'video': forms.FileInput(attrs={
                'accept': 'video/*',
                'class': 'video-upload-input',
                'id': 'video-upload'
            }),
            'grupo_muscular': forms.Select(attrs={
                'class': 'form-select'
            }),
            'exercise_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Ex: Supino Reto, Agachamento Livre...'
            }),
            'instructions': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 4,
                'placeholder': 'Descreva como executar o exercício corretamente...'
            })
        }

    def clean_exercise_name(self):
        value = self.cleaned_data.get('exercise_name')
        if not value:
            raise forms.ValidationError('O campo deve conter um nome.')
        return value

    def clean_grupo_muscular(self):
        value = self.cleaned_data.get('grupo_muscular')
        if not value:
            raise forms.ValidationError('Selecione um grupo muscular.')
        return value

    def clean_video(self):
        video = self.cleaned_data.get('video')
        
        # Se não há vídeo novo e não há vídeo existente, é obrigatório
        if not video and not self.instance.video:
            raise forms.ValidationError('Adicione um vídeo.')
        
        # Se há vídeo, validar o tipo de arquivo
        if video:
            # Verificar extensão do arquivo
            allowed_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
            file_extension = video.name.lower().split('.')[-1]
            
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError(
                    'Formato de vídeo não suportado. Use: MP4, AVI, MOV, WMV, FLV, WebM ou MKV.'
                )
            
            # Verificar tamanho do arquivo (limite de 100MB)
            if video.size > 100 * 1024 * 1024:  # 100MB em bytes
                raise forms.ValidationError('O arquivo de vídeo deve ter no máximo 100MB.')
        
        return video

    def clean_instructions(self):
        value = self.cleaned_data.get('instructions')
        if not value:
            raise forms.ValidationError('Adicione as instruções de execução.')
        return value

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-select'}),
            'comment': forms.Textarea(attrs={
                'class': 'form-textarea', 
                'rows': 4, 
                'placeholder': 'Deixe seu comentário sobre este exercício...'
            }),
        }
        labels = {
            'rating': 'Avaliação',
            'comment': 'Comentário (opcional)',
        }