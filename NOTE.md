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

Creating the database migration script (SQlite which comes eith python):

`python manage.py makemigrations`

(OPTIONAL) you can view the migration to be applied (in SQL) using:

`python manage.py sqlmigrate flashcard 0001` 'flashcard' is the app's name

Applying the migration:

`python manage.py migrate`

Opening interactive python shell with project loaded:

 `python manage.py shell`

---

Useful query syntax: ('Board' is a model name)

Create:

`board = Board()`

Save: 

`board.save()`

Create and Save:

`Board.objects.create(name='...', description='...')`

List:

`Board.objects.all()`

Select:

`Board.objects.get(id=1)`

`Board.objects.get(name='Django)`

---

To use templates:

- create a folder called `templates` where the `manage.py` is
- In the projects `settings.py` under `TEMPLATES` set `DIRS` to `os.path.join(BASE_DIR, 'templates')` or equivalent
- Add `home.html` file in the templates folder
- use the Django Templating Language to dynamically create/update HTML code (e.g.):
    - `{% for entry in entries %}
            <tr>
                <td>{{ entry.from_lang }}</td>
            </tr>
        {% endfor %}`
- in `views.py` return `render` function to provide the `entries`: 
    - `return render(request, 'home.html', {'entries': entries})`   
    
---

Testing

- use `from django.test import TestCase` in project's `test.py`
- use `from django.urls import reverse` (e.g.): 
    - `url = reverse('home') #this is the 'name' field in the urls.py for a url`
- run tests using: `python manage.py test`

---

Static

- Make a folder called `static` in the same place as `manage.py`
- Make another folder in the `static` called `css`
- Add your (bootstrap) css and js files to the folders
- In project's `settings.py` after `STATIC_URL` add:
    - `STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'),]`
- In your .html templates add to the `<head>` section:
    - `<link rel="stylesheet" href="{% static 'css/bootstrap.min.css' %}">`
    - `<script src="{% static 'js/bootstrap.min.js' %}"></script>`
    

---

Admin Account

- Make an admin account using `python manage.py createsuperuser` and follow the instructions 
- You can then sign in at `http://127.0.0.1:8000/admin/`
- To add your model to the admin:
    - In your app's `admin.py` add : `admin.site.register(Board)` (Board is your model (class) name)
    
---

URLs

- Use angled brackets to capture data from the urls e.g. `path('articles/<int:year>/', views.year_archive)`
- more on URLs and how to make your own converter or use regex at: [Django URL Dispatcher](https://docs.djangoproject.com/en/2.2/topics/http/urls/)

---
Modular Templates

- create a `base.html` with place holders using:
    - `{%block blockname %} optional content {% endblock %}`
- extend `base.html`:
    - in `home.html` add `{% extends 'base.html' %}` to the top
    - in `home.html` add your content between `{%block blockname %} home content {% endblock %}` tags
- You can add another .html file using `{% include 'another.html' %}` in between *block* tags

---
Forms

Django has a forms API. **Use it**. It validates (front and backend) in addition to having modelforms.





    

