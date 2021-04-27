# Django Auth

**Using the Third-party app to implement the authentication system:**

## Project Setup:

1.  Create Environment Variable:

        conda create -n  api python=3.8.2

2.  Activate the api
        conda activate api
3.  Install Django:

        pip3 install django
        django-admin --version

4.  Now we create the Django Project:

        django-admin startproject api

5.  Move inside the project:

            cd api
            ls

    We can observe the manage.py file.

6.  Create the app inside the project:

        python manage.py startapp authapp

7.  Install Django RestFramework:

        pip3 install djangorestframework

8.  Install the knox or djoser
        pip3 install django-rest-knox
        pip3 install djoser
9.  Once we are done with the installation, we setup the requirement file.
        touch requirement.txt
        pip3 freeze > requirement.txt
        cat requirement.txt
10. Open settings.py and add the startapp into the `INSTALLED_APPS`,

              INSTALLED_APPS = [
              ...
              'rest_framework',
              'rest_framework.authtoken',
              'knox',
              'djoser',
              'authapp',
            ]

11. Optional - If we make DEBUG = FALSE, then we have to make changes in `ALLOWED_HOSTS = ['*']`.

12. Check whether the project running properly, move to the `manage.py` directory.

                python manage.py makemigrations
                python manage.py migrate
                python manage.py runserver

13. To create superuser:

                python manage.py createsuperuser --email admin@saurabhambar.me --username admin
                Enter
                Type password

14. Run the server and code working properly.

## For Djoser:

14. In the urls.py file (api), import `include`, then write the following path:
        from django.contrib import admin
        from django.urls import path, include
        from .views import index
        urlpatterns = [
            path('admin/', admin.site.urls),
            path('auth/', include('authapp.urls')),
        ]
15. Now create urls.py file in authapp and paste the following code:
16. Check once we have added `authtoken` in the `settings.py` file in `INSTALLED_APPS`:
17. Check once if the server is running with no errors.
        python manage.py runserver
        http://localhost:8000/auth/token/login
18. Now we add `REST_FRAMEWORK` settings in the `settings.py` file:

            REST_FRAMEWORK = {
                'DEFAULT_AUTHENTICATION_CLASSES': (
                    'rest_framework.authentication.BasicAuthentication',
                    'rest_framework.authentication.SessionAuthentication',
                    'rest_framework.authentication.TokenAuthentication',
                    # 'knox.auth.TokenAuthentication',
                ),
                'DEFAULT_PERMISSION_CLASSES': (
                    'rest_framework.permissions.IsAdminUser',
                    'rest_framework.permissions.IsAuthenticated',
                ),
            }

    IsAuthenticated - used to make sure all the apis are authenticated.

19. Run the server and check the urls:

        http://localhost:8000/auth/users/
        http://localhost:8000/auth/users/

20. We can check the created users in the DB Browser, open DB Browser > Open Database > select SQLite file in api > Browser Data > Select auth_user from drop down menu.

We will get the superuser and sign up user data.

21. Try the above URLs with the Postman:

    pictures added in picture folder

22. By default login is thorugh `username` If we want to login through email, we have to make changes in `settings.py` file:
        DJOSER = {
               'LOGIN_FIELD': 'email',
        }
23. We have `Username, Email, Password` for the register page, now if we want to create the our own model,
    We have to make changes in the `models.py` file. We will be using Custom User Model - `AbstactUser`.

USERNAME_FIELD - through which we will sign up.
AbstractUser already have first_name and last_name. We just need to include them in required field.

        from django.db import models
        from django.contrib.auth.models import AbstractUser

        class User(AbstractUser):
            email = models.EmailField(verbose_name='email', max_length=255, unique=True)
            phone = models.CharField(null=True, max_length=255)
            REQUIRED_FIELDS = ['username', 'phone', 'first_name', 'last_name']
            USERNAME_FIELD = 'email'

            def get_username(self) -> str:
                return self.email

24. We create `serializer.py`,
    We will include Djoser serializer, as all authentication running through djoser package.

            from djoser.serializers import UserCreateSerializer, UserSerializer
            from rest_framework import serializers
            from .models import *

            class UserCreateSerializer(UserCreateSerializer):
                    class Meta(UserCreateSerializer.Meta):
                            model = User
                            fileds = ('id', 'email', 'username', 'password', 'first_name', 'last_name', 'phone')

25. Once we have our `Custom User Model`, make changes in the `settings.py` file about which user model to use:
        AUTH_USER_MODEL = 'authapp.User'

It means go to `authapp` and find `User` model for the `authapp`

26. To write the password again, in `settings.py` file:
        DJOSER = {
                'LOGIN_FIELD': 'email',
                'USER_CREATE_PASSWORD_RETYPE': True,
        }
27. We have to include the serializer in the Djoser setting:
        DJOSER = {
               'LOGIN_FIELD': 'email',
               # 'USER_CREATE_PASSWORD_RETYPE': True,
               'SERIALIZER': {
                       'user_create': 'authapp.serializers.UserCreateSerializer',
                       'user': 'authapp.serializers.UserCreateSerializer',
                       # 'current_user': 'authentication.serializers.CurrentUserSerializer',
               },
        }
28. Run server:

        python manage.py makemigraions
        python manage.py makemigraions authapp
        python manage.py migrate
        python manage.py runserver

29. Now to add **restriction** to the project, So only authorized user can access:
30. Add the code in `urls.py` file:
        path('restricted/', views.restricted),
31. Create a function in `views.py`:

        from django.shortcuts import render
        from rest_framework.decorators import api_view, permission_classes
        from rest_framework.permissions import IsAuthenticated
        from rest_framework.response import Response
        from rest_framework import status
        # Create your views here.


        @api_view(['GET'])
        def restricted(request, *args, **kwargs):
            return Response(data="Only for logged in User", status=status.HTTP_200_OK)

32. Now check these using the following URLs:

        http://localhost:8000/auth/restricted/

33. All API points we encounter in this project:

        http://localhost:8000/auth/users/
        http://127.0.0.1:8000/auth/token/login
        http://127.0.0.1:8000/auth/users/me/
        http://127.0.0.1:8000/auth/token/logout/
        http://localhost:8000/auth/restricted/

Error:

1. django.db.migrations.exceptions.InconsistentMigrationHistory: Migration **admin.0001_initial** is applied before its dependency accounts.0001_initial on database 'default'.

The solution is to undo your existing migrations that depend on AUTH_USER_MODEL as mentioned in this answer. In case you are trying to undo migrations for admin, auth, contenttypes and sessions and you get an error like:

- First of all comment out/undo `AUTH_USER_MODEL` in `settings.py` if you had changed that.
- Secondly comment out/undo your django app(`authapp`) that contains new `AUTH_MODEL` from `INSTALLED_APPS` in `settings.py`.
- Now you should be able to undo migrations for `auth, admin, contenttypes and sessions` as:

        python manage.py migrate admin zero
        python manage.py migrate auth zero
        python manage.py migrate contenttypes zero
        python manage.py migrate sessions zero


- Now add your auth model app(`authapp`) to INSTALLED_APPS and set `AUTH_USER_MODEL` in your `settings.py` again.
- Run: python `manage.py migrate authapp`, you may need to make migrations for your auth model app as well: `python manage.py makemigrations authapp`

Apply all migrations that you undo by: `python manage.py migrate`.

You are all done.

**Note: You will lose all existing users present in database.**

2. Sometimes error can be solved by deleting the sqlite and migrations file.
