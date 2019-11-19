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

- create a form.py and subclass either Form or ModelForm
- if you are using a ModelForm to directly create a Model you can choose which attributes of the model to be populated 
by the form. Use a `class Meta:` inside your subclassed form class set `model` and `fields` attributes of the Meta class.
- **view**
    - for view function use [This Ofiicial Layout Example](https://docs.djangoproject.com/en/2.2/topics/forms/#the-view)
    - Notice that the forms API will make validation easy. look into `form.is_valid()` and `form.cleaned_data`
- **template**
    - you can access the form in your template through the `{{ form }}` variable and even loop over the fields in the form.
    - you should always include a `{% csrf_token %}` inside your form tags.
    - The form variable does not include the HTML <form> tags or the submit button you should write them yourself.

---
Authentication

There are a log of moving parts here but these are some of the keywords and highlights.

- Do the authentication as an app. Make an app called `accounts`.
- Add it to the `INSTALLED_APPS` in settings.py
- For signing up:
    - Add the url for `signup`.`
    - You want the view to return the form:
        - There is already a `from django.contrib.auth.forms import UserCreationForm` for creating new Users
- In templates: `{% user.is_authenticated %}` 
- In views.py: `request.user.is_authenticated`
- For logging in:
    - `LOGIN_REDIRECT_URL = 'home'` in settings.py
    - `path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login')` you don't have to make 
    your own login view
- For logging out:
    - `LOGOUT_REDIRECT_URL = 'home'` in settings.py
    - `path('logout/', auth_views.LogoutView.as_view(), name='logout')` you don't have to make your own view function.
    
---

Protecting views from anonymous users

- use `from django.contrib.auth.decorators import login_required` to import a decorator to put on top of the view 
function you are trying to protect. if an unauthorized user tries to access a url they will be redirected to the login
page.

- in `settings.py` add `LOGIN_URL = 'login'` to the end of the file

- to redirect to the original page after logging in you can use the **next** input in the log in form:
as follows: `<input type="hidden" name="next" value="{{ next }}">` 

---

# Deployement to Heroku:

- [useful link for Postgre db](https://medium.com/agatha-codes/9-straightforward-steps-for-deploying-your-django-app-with-heroku-82b952652fb4)






    

