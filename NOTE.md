Django Tutorials:

[Vitor Freitas](https://simpleisbetterthancomplex.com/series/2017/09/04/a-complete-beginners-guide-to-django-part-1.html#starting-a-new-project)


---

Start a new project:

`django-admin startproject myproject`

Run the server:

`python manage.py runserver`

Create an app in the project:

`django-admin startapp boards`

Add the app in the projects *settings.py* under *INSTALLED_APPS*

*views.py* has functions with input: `HttpRequest` and output: `HttpResponse`

*urls.py* adds a function in the views.py as an endpoint like:

`path('', views.home, name='home')`

---




