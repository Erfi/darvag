from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView, ListView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from flashcard.models import Entry, Deck
from flashcard.forms import NewEntryForm, NewDeckForm

from tags.models import Tag
from tags.forms import TagFilterForm
from tags.filters import TagFilter



def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


def lang_entry(request, from_lang):
    entries = Entry.objects.filter(from_lang=from_lang)
    return render(request, 'home.html', {'entries': entries})


@login_required
def add_entry(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entry = Entry.objects.create(from_lang=deck.from_lang,
                                         to_lang=deck.to_lang,
                                         from_word=form.cleaned_data['from_word'],
                                         to_word=form.cleaned_data['to_word'],
                                         from_example=form.cleaned_data['from_example'],
                                         deck=deck,
                                         created_by=request.user)
            entry.save()
            return redirect('view_deck', deck_id=deck.id)
    else:
        form = NewEntryForm()
    return render(request, 'new_entry_form.html', {'form': form, 'deck_id': deck_id})


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
def view_deck_filter(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    entries = deck.entries.all()
    tags_queryset = Tag.objects.filter(created_by=request.user)

    if request.method == 'POST':
        form = TagFilterForm(request.POST, tags_queryset=tags_queryset)
        if form.is_valid() and form.is_bound:
            print(f'cleaned_data: {form.cleaned_data}')
            tag_filter = TagFilter(queryset=entries)
            entries = tag_filter.filter_entries(cleaned_data=form.cleaned_data)
    else:
        form = TagFilterForm(tags_queryset=tags_queryset)
    return render(request, 'view_deck.html', {'form': form, 'entries': entries, 'deck': deck})


@method_decorator(login_required, name='dispatch')
class EntryListView(ListView):
    model = Entry
    context_object_name = 'entries'
    template_name = 'view_deck.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        deck_id = self.kwargs.get('deck_id')
        deck = get_object_or_404(Deck, id=deck_id)
        return queryset.filter(deck=deck)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        deck_id = self.kwargs.get('deck_id')
        deck = get_object_or_404(Deck, id=deck_id)
        context['deck'] = deck
        return context


@method_decorator(login_required, name='dispatch')
class DeckUpdateView(UpdateView):
    model = Deck
    fields = ['from_lang', 'to_lang']
    template_name = 'edit_deck.html'
    pk_url_kwarg = 'deck_id'
    context_object_name = 'deck'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.created_by = self.request.user
        deck.save()
        return redirect('dashboard')


@method_decorator(login_required, name='dispatch')
class DeckDeleteView(DeleteView):
    model = Deck
    template_name = 'delete_deck.html'
    pk_url_kwarg = 'deck_id'
    context_object_name = 'deck'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class EntryUpdateView(UpdateView):
    model = Entry
    fields = ['from_word', 'to_word', 'from_example']
    template_name = 'edit_entry.html'
    pk_url_kwarg = 'entry_id'
    context_object_name = 'entry'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        entry = form.save()
        return redirect('view_deck', deck_id=entry.deck.id)


@method_decorator(login_required, name='dispatch')
class EntryDeleteView(DeleteView):
    model = Entry
    template_name = 'delete_entry.html'
    pk_url_kwarg = 'entry_id'
    context_object_name = 'entry'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def get_success_url(self):
        deck_id = self.kwargs.get('deck_id')
        return reverse_lazy('view_deck', kwargs={'deck_id': deck_id})
