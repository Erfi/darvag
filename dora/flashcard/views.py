from django.shortcuts import render, redirect
from flashcard.forms import NewEntryForm
from flashcard.models import Entry
from django.contrib.auth.decorators import login_required


def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def lang_entry(request, from_lang):
    entries = Entry.objects.filter(from_lang=from_lang)
    return render(request, 'home.html', {'entries': entries})

@login_required
def add_entry(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = Entry.objects.create(from_lang=form.cleaned_data['from_lang'],
                                         to_lang=form.cleaned_data['to_lang'],
                                         from_word=form.cleaned_data['from_word'],
                                         to_word=form.cleaned_data['to_word'],
                                         from_example=form.cleaned_data['from_example'],
                                         created_by=request.user)
            entry.save()
            return redirect('home')
    else:
        form = NewEntryForm()
    return render(request, 'new_entry_form.html', {'form': form})



