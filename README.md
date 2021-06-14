# Stadia Client

This web application uses django to implement a seat booking process for events. The app is built to simulate this process but not intended for deployment purposes.

## How to run the application

First ensure python is installed on your system, once confirmed run the following

`pip install -r requirements.txt`

once this is done open you current working directory (CWD) on your project terminal and type `dir`. Ensure that `manage.py` is present in the current working directory. 

If it is not it is either you're in the StadiaClient app -- of which you need to type `cd ../`  on you CWD -- or you are directly outside you project folder -- of which you need to type `cd Stadia_client`.

Once in the current directory you will enter this series of commands

```commandline
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

After creating a super user where you fill all the necessary information, you run your django server as thus:

```commandline
python manage.py runserver
```

At this you can explore this web application as you like and even make changes.
