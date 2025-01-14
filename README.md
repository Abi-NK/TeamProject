# CS2810 Team Project: Team 5

## Test folder location: posSystem/tests

## Introduction

The COO of Oaxaca has reached out to us to see if there is some way we can help them mitigate
their issues by reducing the staffing and/or training needs of their restaurants with technology. Our
goal is to look at their existing processes and identify ways in which we can use technology to help
them grow faster.

<br>

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.



### Prerequisites




```
Python
```
```
Django
```
<br>


### Installing

First install Python:
```
$ sudo apt-get update
$ sudo apt-get install python3.6
```
Then install Pip:

```
$ sudo easy_install pip
```

Then install virtualenv:

```
$ sudo pip install virtualenv
```

Lastly install django:

```
$ sudo pip install django
```

You can test that the installation was successful by typing:

```
$ django-admin.py version

2.0.1
```

<br>


## Running the tests

Django's unit tests use a Python standard library module: **unittest**.

Tests that require a database will not use the real production database, separate blank databases are created for the tests and then destroyed after the tests have been completed, regardless of whether the tests pass or fail.
 
**Tests are located within the posSystem/tests folder as a tests.py file.**


Run all tests within the project using the test command of the project’s manage.py utility:

```
$ python manage.py test
```

and then you will see something like this:

```

----------------------------------------------------------------------
Ran 32 tests in 0.018s

OK

```

<br>

## Coding style

* [PEP 8](https://www.python.org/dev/peps/pep-0008/) -  Python style guide using 120 maximum characters per line


<br>


## Deployment

To run the server type the following command:

```
$ python manage.py runserver
```

then you will see something like this:

```
Performing system checks...

System check identified no issues (0 silenced).
February 22, 2018 - 01:41:54
Django version 2.0.1, using settings 'server.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```


<br>


## Built With

* [Django](https://www.djangoproject.com/) -  Web framework

<br>


## Contributing

1. Create your feature branch: `git checkout -b my-new-feature`
2. Commit your changes: `git commit -m 'Add some feature'`
3. Push to the branch: `git push origin my-new-feature`
4. Submit a pull request

<br>


## Authors

- **Abi Nand Kumar** -------- [Abi-NK](https://github.com/Abi-NK)
- **Bryn Davies** ---------------------- [ManRay99](https://github.com/ManRay99) and [H09bdavies](https://github.com/H09bdavies)
- **Henry Gilbert** -------------------- [ausanc](https://github.com/ausanc)
- **Khalil Kablan** -------------------- [kkablan](https://github.com/kkablan)
- **Rodney Olav C. Melby** -------- [RHUL-INFO-SEC-MASTERS](https://github.com/RHUL-INFO-SEC-MASTERS)
- **Tom McGregor** ------------------ [TomMcGregor](https://github.com/TomMcGregor)


See the list of [contributors](https://github.com/RHUL-CS-Projects/TeamProject2018_05/graphs/contributors) who participated in this project.
