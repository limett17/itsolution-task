from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from .models import Quote, Source
from .forms import QuoteForm
import random


# Create your views here.
def random_quote(request):
    quotes = Quote.objects.all()
    quote = random.choices(quotes, weights=[q.prob_rate for q in quotes], k=1)[0]
    print(request.META)
    return render(request, "quotes/random_quote.html", {"quote": quote})


def top_quotes(request):
    return render(request, "topQuote.html")


def add_quote(request):
    form = QuoteForm()
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            source_name = form.cleaned_data['source_name']
            source_type = form.cleaned_data['source_type']
            source, _ = Source.objects.get_or_create(name=source_name, type=source_type)

            quote = form.save(commit=False)
            quote.source = source
            quote.save()
            messages.success(request, "Цитата добавлена успешно!")
            print("Добавляем цитату")
            form = QuoteForm()
        else:
            print(form.errors)

    return render(request, "addQuote.html", {"form": form})
