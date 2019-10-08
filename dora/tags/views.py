from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from tags.models import Tag


@method_decorator(login_required, name='dispatch')
class TagListView(ListView):
    model = Tag
    context_object_name = 'tags'
    template_name = 'tags_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class TagCreateView(CreateView):
    model = Tag
    fields = ['name']
    template_name = 'tags_create.html'

    def form_valid(self, form):
        tag = form.save(commit=False)
        tag.created_by = self.request.user
        tag.save()
        return redirect('list_tags')


@method_decorator(login_required, name='dispatch')
class TagUpdateView(UpdateView):
    model = Tag
    fields = ['name']
    template_name = 'tags_update.html'
    pk_url_kwarg = 'tag_id'
    success_url = reverse_lazy('list_tags')
    context_object_name = 'tag'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)


@method_decorator(login_required, name='dispatch')
class TagDeleteView(DeleteView):
    model = Tag
    template_name = 'tags_delete.html'
    pk_url_kwarg = 'tag_id'
    success_url = reverse_lazy('list_tags')
    context_object_name = 'tag'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)
