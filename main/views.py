from django.shortcuts import render
from django.http import HttpResponse
from .models import Quote, Source
from .forms import QuoteForm
import random


# Create your views here.
def random_quote(request):
    quotes = Quote.objects.all()
    quote = random.choice(quotes) if quotes else None
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
            print("Добавляем цитату")
        else:
            print(form.errors)

    return render(request, "addQuote.html", {"form": form})
