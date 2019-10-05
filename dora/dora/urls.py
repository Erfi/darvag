"""dora URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from flashcard import views as flashcard_views
from accounts import views as account_views

urlpatterns = [
    path('', flashcard_views.home, name='home'),
    path('signup/', account_views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset.html',
        email_template_name='password_reset_email.html',
        subject_template_name='password_reset_subject.txt'),
         name='password_reset'),
    path('reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='password_reset_done.html'),
         name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
            auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),
            name='password_reset_confirm'),
    path('reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
    path('settings/password/', auth_views.PasswordChangeView.as_view(template_name='password_change.html'),
         name='password_change'),
    path('settings/password/done', auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html'),
         name='password_change_done'),
    path('admin/', admin.site.urls),
    path('user/dashboard/', flashcard_views.dashboard, name='dashboard'),
    path('deck/add/', flashcard_views.add_deck, name='add_deck'),
    # path('deck/<int:deck_id>/', flashcard_views.EntryListView.as_view(), name='view_deck'),

    path('deck/<int:deck_id>/', flashcard_views.view_deck_filter, name='view_deck'),

    path('deck/<int:deck_id>/edit/', flashcard_views.DeckUpdateView.as_view(), name='edit_deck'),
    path('deck/<int:deck_id>/delete/', flashcard_views.DeckDeleteView.as_view(), name='delete_deck'),
    path('deck/<int:deck_id>/add/', flashcard_views.add_entry, name='add_entry'),
    path('deck/<int:deck_id>/entry/<int:entry_id>/edit/', flashcard_views.EntryUpdateView.as_view(), name='edit_entry'),
    path('deck/<int:deck_id>/entry/<int:entry_id>/delete/', flashcard_views.EntryDeleteView.as_view(),
         name='delete_entry')
]
