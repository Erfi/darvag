from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from flashcard.forms import NewEntryForm
from flashcard.models import Entry


def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def lang_entry(request, from_lang):
    entries = Entry.objects.filter(from_lang=from_lang)
    return render(request, 'home.html', {'entries': entries})


def add_entry(request):
    user = User.objects.first() #TODO: change to the authenticated user
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = Entry.objects.create(from_lang=form.cleaned_data['from_lang'],
                                         to_lang=form.cleaned_data['to_lang'],
                                         from_word=form.cleaned_data['from_word'],
                                         to_word=form.cleaned_data['to_word'],
                                         from_example=form.cleaned_data['from_example'],
                                         created_by=user)
            entry.save()
            return redirect('home')
    else:
        form = NewEntryForm()
    return render(request, 'entry_form.html', {'form': form})



