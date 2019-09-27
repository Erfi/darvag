from django.shortcuts import render, redirect
from flashcard.forms import NewEntryForm, NewDeckForm
from flashcard.models import Entry, Deck
from django.contrib.auth.decorators import login_required


def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def lang_entry(request, from_lang):
    entries = Entry.objects.filter(from_lang=from_lang)
    return render(request, 'home.html', {'entries': entries})


@login_required
def add_entry(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = Entry.objects.create(from_lang=form.cleaned_data['from_lang'],
                                         to_lang=form.cleaned_data['to_lang'],
                                         from_word=form.cleaned_data['from_word'],
                                         to_word=form.cleaned_data['to_word'],
                                         from_example=form.cleaned_data['from_example'],
                                         deck=deck,
                                         created_by=request.user)
            entry.save()
            return redirect('home')
    else:
        form = NewEntryForm()
    return render(request, 'new_entry_form.html', {'form': form})


@login_required
def dashboard(request):
    users_decks = Deck.objects.filter(created_by=request.user)
    return render(request, 'dashboard.html', {'decks': users_decks})


@login_required
def add_deck(request):
    if request.method == 'POST':
        form = NewDeckForm(request.POST)
        if form.is_valid():
            deck = Deck.objects.create(from_lang=form.cleaned_data['from_lang'],
                                       to_lang=form.cleaned_data['to_lang'],
                                       created_by=request.user)
            deck.save()
            return redirect('dashboard')
    else:
        form = NewDeckForm()
    return render(request, 'new_deck_form.html', {'form': form})


@login_required
def view_deck(request, deck_id):
    deck = Deck.objects.get(id=deck_id)
    entries = deck.entries.all()
    return render(request, 'view_deck.html', {'entries': entries, 'deck':deck})