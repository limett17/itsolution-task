from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Quote, Source, ViewCount, RatingCount
from .forms import QuoteForm
from django.http import JsonResponse
import json
import random


def random_quote(request):
    quotes = Quote.objects.all()
    quote = random.choices(quotes, weights=[q.prob_rate for q in quotes], k=1)[0]
    if not request.session.session_key:
        request.session.save()
    session_key = request.session.session_key
    try:
        rating = RatingCount.objects.get(quote=quote, session=session_key)
        user_rating = rating.value
    except RatingCount.DoesNotExist:
        user_rating = 0
    is_views = ViewCount.objects.filter(quote=quote, session=session_key)
    if is_views.count() == 0 and str(session_key) != 'None':
        views = ViewCount()
        views.session = session_key
        views.quote = quote
        views.save()
        quote.views += 1
        quote.save()
    return render(request, "quotes/random_quote.html", {"quote": quote, "user_rating": user_rating})


@require_POST
def rate_quote(request):
    data = json.loads(request.body)
    quote_id = data.get("quote_id")
    value = data.get("value")
    session_key = request.session.session_key or request.session.save()
    try:
        quote = Quote.objects.get(id=quote_id)
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=404)

    existing = RatingCount.objects.filter(quote_id=quote_id, session=session_key).first()

    if existing:
        if existing.value == value:
            existing.delete()
            if value == 1:
                quote.likes = max(quote.likes - 1, 0)
            else:
                quote.dislikes = max(quote.dislikes - 1, 0)
            current_vote = None
        else:
            if existing.value == 1:
                quote.likes = max(0, quote.likes - 1)
                quote.dislikes += 1
            elif existing.value == -1:
                quote.dislikes = max(0, quote.dislikes - 1)
                quote.likes += 1
            existing.value = value
            existing.timestamp = timezone.now()
            current_vote = value
            existing.save()
    else:
        RatingCount.objects.create(quote=quote, session=session_key, value=value)
        if value ==1:
            quote.likes += 1
        elif value ==-1:
            quote.dislikes += 1
        current_vote = value
    quote.save()
    return JsonResponse({
        'message': 'Голос учтён!',
        'likes': quote.likes,
        'dislikes': quote.dislikes,
        "current_vote": current_vote
    })


def top_quotes(request):
    quotes = Quote.objects.order_by("-likes")[:10]
    return render(request, "quotes/topQuote.html", {"quotes": quotes})


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

    return render(request, "quotes/addQuote.html", {"form": form})
