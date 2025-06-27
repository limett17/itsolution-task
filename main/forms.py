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
        if source_name and source_type:
            try:
                source = Source.objects.get(name=source_name, type=source_type)
                if Quote.objects.filter(source=source).count() >= 3:
                    raise ValidationError("This source already has 3 quotes!")
            except Source.DoesNotExist:
                pass
        return cleaned_data
