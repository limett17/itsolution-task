from django import forms
from .models import Quote, Source
from django.core.exceptions import ValidationError


class QuoteForm(forms.ModelForm):
    source_name = forms.CharField(label="Source name")
    source_type = forms.ChoiceField(choices=Source.SOURCE_TYPES)

    class Meta:
        model = Quote
        fields = ('quote', 'source_name', 'source_type', 'prob_rate')

    def clean(self):
        cleaned_data = super().clean()
        source_name = cleaned_data.get('source_name')
        source_type = cleaned_data.get('source_type')
        prob = cleaned_data.get('prob_rate')
        if (prob<=0):
            raise ValidationError("Вы ввели вероятность меньше или равной нулю. Ваша цитата не будет отображаться при "
                                  "таком вводе. Введите число в диапазоне от 0 до 1.")
        elif (prob>=1):
            raise ValidationError("Вы ввели вероятность равной или больше 1. Будет как-то нечестно отображать всего "
                                  "одну цитату, не думаете? Введите число в диапазоне от 0 до 1.")
        if source_name and source_type:
            try:
                source = Source.objects.get(name=source_name, type=source_type)
                if Quote.objects.filter(source=source).count() >= 3:
                    raise ValidationError("This source already has 3 quotes!")
            except Source.DoesNotExist:
                pass
        return cleaned_data
