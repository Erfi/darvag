from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView, ListView, CreateView
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from flashcard.models import Entry, Deck
from flashcard.forms import CreateEntryForm, UpdateEntryForm

from tags.models import Tag
from tags.forms import TagFilterForm
from tags.filters import TagFilter


def home(request):
    entries = Entry.objects.all()
    return render(request, 'home.html', {'entries': entries})


@method_decorator(login_required, name='dispatch')
class DeckListView(ListView):
    model = Deck
    template_name = 'dashboard.html'
    context_object_name = 'decks'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class DeckCreateView(CreateView):
    model = Deck
    fields = ['name']
    template_name = 'new_deck_form.html'

    def form_valid(self, form):
        deck = form.save(commit=False)
        deck.created_by = self.request.user
        deck.save()
        return redirect('dashboard')


@method_decorator(login_required, name='dispatch')
class DeckUpdateView(UpdateView):
    model = Deck
    fields = ['name']
    template_name = 'edit_deck.html'
    pk_url_kwarg = 'deck_id'
    context_object_name = 'deck'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        form.save()
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
class EntryListView(View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.template_name = 'view_deck.html'

    def get_context_data(self):
        deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        entries = deck.entries.all()
        tags_queryset = Tag.objects.filter(created_by=self.request.user)
        return {'deck': deck, 'entries': entries, 'tags_queryset': tags_queryset}

    def get(self, request, *args, **kwargs):
        data = self.get_context_data()
        form = TagFilterForm(tags_queryset=data['tags_queryset'])
        return render(request, self.template_name, {'form': form, 'entries': data['entries'], 'deck': data['deck']})

    def post(self, request, *args, **kwargs):
        data = self.get_context_data()
        entries = data['entries']
        form = TagFilterForm(request.POST, tags_queryset=data['tags_queryset'])
        if form.is_valid():
            tag_filter = TagFilter(queryset=data['entries'])
            used_tags = Tag.get_instances_from_representations(rep_list=form.cleaned_data['tags'], user=request.user)
            entries = tag_filter.filter_entries(tags=used_tags)
        return render(request, self.template_name, {'form': form, 'entries': entries, 'deck': data['deck']})


@method_decorator(login_required, name='dispatch')
class EntryCreateView(CreateView):
    model = Entry
    form_class = CreateEntryForm
    template_name = 'new_entry_form.html'
    success_url = reverse_lazy('view_deck', )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tag_queryset'] = Tag.objects.filter(created_by=self.request.user).all()
        return kwargs

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['deck_id'] = self.kwargs['deck_id']
        return kwargs

    def form_valid(self, form):
        deck = get_object_or_404(Deck, id=self.kwargs['deck_id'])
        entry = form.save(commit=False)
        entry.deck = deck
        entry.from_lang = deck.from_lang
        entry.to_lang = deck.to_lang
        entry.created_by = self.request.user
        entry.save()
        # --- now that entry has an id we can add the m2m relationship ---
        tags = Tag.get_instances_from_representations(rep_list=form.cleaned_data['tags'], user=self.request.user)
        entry.tags.set(tags)
        entry.save()
        return redirect('view_deck', deck_id=deck.id)


@method_decorator(login_required, name='dispatch')
class EntryUpdateView(UpdateView):
    model = Entry
    form_class = UpdateEntryForm
    template_name = 'edit_entry.html'
    pk_url_kwarg = 'entry_id'
    context_object_name = 'entry'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        entry = form.save(commit=False)
        tags = Tag.get_instances_from_representations(rep_list=form.cleaned_data['tags'], user=self.request.user)
        entry.tags.set(tags)
        entry.save()

        return redirect('view_deck', deck_id=entry.deck.id)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['tag_queryset'] = Tag.objects.filter(created_by=self.request.user).all()
        return kwargs


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
