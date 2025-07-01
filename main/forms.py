from django import forms
from .models import Quote, Source
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(label="Название источника")
    source_type = forms.ChoiceField(choices=Source.SOURCE_TYPES, label="Тип источника")

    class Meta:
        model = Quote
        fields = ('quote', 'source_name', 'source_type', 'prob_rate')
        labels = {
            'quote': "Цитата",
            'source_name': 'Название источника',
            'source_type': 'Тип источника',
            'prob_rate': 'Вероятность'
        }

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')
        quote = cleaned_data.get('quote')
        prob = cleaned_data.get('prob_rate')
        if prob <= 0:
            raise ValidationError("Вы ввели вероятность меньше или равной нулю. Ваша цитата не будет отображаться при "
                                  "таком вводе. Введите число в диапазоне от 1 до 100.")
        elif prob > 100:
            raise ValidationError("Вы ввели вероятность больше 100. Будет как-то нечестно отображать всего "
                                  "одну цитату, не думаете? Введите число в диапазоне от 1 до 100.")
        if quote and source_name and source_type:
            try:
                source = Source.objects.get(name=source_name, type=source_type)
                if Quote.objects.filter(quote=quote, source=source).exists():
                    raise ValidationError("Такая цитата уже существует для этого источника!")
                if Quote.objects.filter(source=source).count() >= 3:
                    raise ValidationError("У этого источника уже имеется 3 цитаты! Больше добавить нельзя!")
            except Source.DoesNotExist:
                pass
        return cleaned_data


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)