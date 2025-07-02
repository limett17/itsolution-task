from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate, logout
from .models import Quote, Source, ViewCount, RatingCount
from .forms import QuoteForm, SignUpForm, LoginForm
from django.http import JsonResponse
import json
import random


def random_quote(request):
    quotes = Quote.objects.all()
    quote = random.choices(quotes, weights=[q.prob_rate for q in quotes], k=1)[0]

    user_rating = 0
    if request.user.is_authenticated:
        user = request.user

        try:
            rating = RatingCount.objects.get(quote=quote, user=user)
            user_rating = rating.value
        except RatingCount.DoesNotExist:
            user_rating = 0

        is_views = ViewCount.objects.filter(quote=quote, user=user)
        if not is_views.exists():
            views = ViewCount(quote=quote, user=user)
            views.save()
        view_count = ViewCount.objects.filter(quote=quote).count()
        quote.views = view_count
        quote.save()
    return render(request, "quotes/random_quote.html", {"quote": quote, "user_rating": user_rating})


@require_POST
def rate_quote(request):
    data = json.loads(request.body)
    quote_id = data.get("quote_id")
    value = data.get("value")
    try:
        quote = Quote.objects.get(id=quote_id)
    except Quote.DoesNotExist:
        return JsonResponse({'error': 'Quote not found'}, status=404)
    user_rating = 0
    if request.user.is_authenticated:
        user = request.user

        existing = RatingCount.objects.filter(quote_id=quote_id, user=user).first()
        #print(existing.value)
        print(value)
        if existing:
            if existing.value == value:
                existing.delete()
                if value == 1:
                    quote.likes = max(quote.likes - 1, 0)
                else:
                    quote.dislikes = max(quote.dislikes - 1, 0)
                current_vote = 0

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
            RatingCount.objects.create(quote=quote, user=user, value=value)
            if value == 1:
                quote.likes += 1
            elif value == -1:
                quote.dislikes += 1
            current_vote = value
        quote.save()
        return JsonResponse({
            'message': 'Голос учтён!',
            'likes': quote.likes,
            'dislikes': quote.dislikes,
            "current_vote": current_vote
        })
    else:
        return JsonResponse({
            'error': 'Вы не авторизованы. Войдите, чтобы оценить цитату.',
            'likes': quote.likes,
            'dislikes': quote.dislikes,
        }, status=401)


def top_quotes(request):
    top = Quote.objects.order_by("-likes")[:10]
    latest = Quote.objects.order_by("-timestamp")[:10]
    top_ratings_dict = {}
    latest_ratings_dict = {}
    if request.user.is_authenticated:
        top_ratings = RatingCount.objects.filter(user=request.user, quote__in=top)
        latest_ratings = RatingCount.objects.filter(user=request.user, quote__in=latest)
        top_ratings_dict = {r.quote_id: r.value for r in top_ratings}
        latest_ratings_dict = {r.quote_id: r.value for r in latest_ratings}

    return render(request, "quotes/topQuote.html", {
        "top_quotes": top,
        "latest_quotes": latest,
        "top_ratings": top_ratings_dict,
        "latest_ratings": latest_ratings_dict})


@login_required
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
            quote.author = request.user
            quote.save()
            messages.success(request, "Цитата добавлена успешно!")
            print("Добавляем цитату")
            form = QuoteForm()
        else:
            print(form.errors)

    return render(request, "quotes/addQuote.html", {"form": form})


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Вы успешно зарегистрированы!")
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'quotes/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Вы успешно авторизованы!")
                return redirect('/')
    return render(request, "quotes/login.html", {'form': form})


@login_required
def profile_info(request):
    return render(request, "profile_templates/profile_info.html")


@login_required
def my_quotes(request):
    quotes = Quote.objects.filter(author=request.user).order_by("-timestamp")
    ratings = RatingCount.objects.filter(user=request.user, quote__in=quotes)
    ratings_dict = {r.quote_id: r.value for r in ratings}
    return render(request, "profile_templates/my_quotes.html", {
        "quotes": quotes,
        "top_ratings": ratings_dict,
    })


@login_required
def my_rated_quotes(request):
    rated = RatingCount.objects.filter(user=request.user).select_related("quote").order_by("-timestamp")
    quotes = [r.quote for r in rated]
    ratings = RatingCount.objects.filter(user=request.user, quote__in=quotes)
    ratings_dict = {r.quote_id: r.value for r in ratings}
    return render(request, "profile_templates/my_rated_quotes.html", {
        "quotes": quotes,
        "top_ratings": ratings_dict,
    })


@login_required
def my_history(request):
    viewed = ViewCount.objects.filter(user=request.user).select_related("quote").order_by("-timestamp")
    quotes = [r.quote for r in viewed]
    ratings = RatingCount.objects.filter(user=request.user, quote__in=quotes)
    ratings_dict = {r.quote_id: r.value for r in ratings}

    return render(request, "profile_templates/my_history.html", {
        "quotes": quotes,
        "top_ratings": ratings_dict,
    })


def logout_view(request):
    logout(request)
    messages.success(request, "Вы успешно вышли.")
    return redirect('/')
