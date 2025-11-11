from django import forms
from .models import Paste, Comment

class PasteForm(forms.ModelForm):
    class Meta:
        model = Paste
        fields = ['title', 'content', 'topic', 'visibility', 'expires_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название пасты...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-input code-textarea',
                'placeholder': 'Введите текст вашей пасты...',
                'rows': 15,
                'spellcheck': 'false'
            }),
            'topic': forms.Select(attrs={'class': 'form-input'}),
            'visibility': forms.Select(attrs={'class': 'form-input'}),
            'expires_at': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
        }
        labels = {
            'title': 'Заголовок пасты',
            'content': 'Содержание',
            'topic': 'Тема',
            'visibility': 'Видимость',
            'expires_at': 'Срок действия (необязательно)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически загружаем темы
        from .models import Topic
        self.fields['topic'].queryset = Topic.objects.filter(is_public=True)
        self.fields['topic'].empty_label = "Без темы"
        
        # Устанавливаем начальные значения
        self.fields['visibility'].initial = 'public'
        # УДАЛИТЕ эту строку: self.fields['syntax'].initial = 'text'
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': "Оставьте комментарий...",
                'rows':3
            })
        }
        labels = {
            'content': "Комментарий"
        }