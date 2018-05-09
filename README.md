# Piłka na kartce (paper soccer)

**Opis**

* Piłka to gra strategiczna przeznaczona dla dwóch osób. Jest rozgrywana na boisku o wymiarach 8x10 kratek i celem gry jest... zdobycie bramki :) Więcej informacji: [Wikipedia](https://pl.wikipedia.org/wiki/Piłkarzyki_na_kartce), [Kurnik](https://www.kurnik.pl/pilka/zasady.phtml)

* Od 2004 r. kurnik zapisuje partie użytkowników. Umożliwia to wygodne przeglądanie rozegranych gier. I na tym niestety kończą się wszystkie możliwości serwisu :(

**papersoccer.pl**

* To strona internetowa napisana przy użyciu frameworka Django 2.0. Oprócz możliwości przeglądania zarchiwizowanych partii z kurnika, serwis wprowadza nowe funkcje:

* możliwość obracania boiska
* wygodne dodawanie/zarządzanie schematami
* orlik treningowy z możliwością zapisania własnej partii
* mazak Gmocha - wyznaczanie wszystkich możliwych wariantów ruchu
* biblioteczka: schematów i analizowanych partii (+ partie treningowe)
* statystyki graczy (uwzględniające średni ranking)

**Screenshots**

<img src='https://raw.github.com/slunzok/papersoccer/master/static/screenshots/001_002.png'/>

**Wymagania**

* Django 2.0.4

**Instalacja (uberspace.de)**

    # instalacja Django, artykuł na Wiki: http://uberspace.de/dokuwiki/cool:django

    $ git clone https://github.com/slunzok/papersoccer
    $ cd papersoccer

    # zmień wartości zmiennych: ALLOWED_HOSTS, DATABASES, STATIC_ROOT, STATIC_URL
    $ vim papersoccer/settings.py

    # utwórzu katalog 'static' w STATIC_ROOT i skopiuj do niego pliki z 'static'
    # np. jeśli nazwa użytkownika: 'foo', a DJANGOURL: django.foo.crux.uberspace.de
    $ mkdir /var/www/virtual/foo/django.foo.crux.uberspace.de
    $ cp -a static/. /var/www/virtual/foo/django.foo.crux.uberspace.de/static/
    
    $ python3.4 manage.py makemigrations
    $ python3.4 manage.py migrate

**Licencja**

* Kod źródłowy jest dostępny na licencji MIT.

