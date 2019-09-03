from django.shortcuts import render
from django.http import HttpResponse
from flashcard.models import Entry


def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def lang_entry(request, from_lang):
    entries = Entry.objects.filter(from_lang=from_lang)
    return render(request, 'home.html', {'entries': entries})


def add_entry(request):
    return render(request, 'entry_form.html')



