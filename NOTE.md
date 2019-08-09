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
- 

