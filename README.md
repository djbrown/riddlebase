# RiddleBase

[![Travis-CI Build Status](https://travis-ci.org/djbrown/riddlebase.svg?branch=master)](https://travis-ci.org/djbrown/riddlebase)
[![Docker Hub Build Status](https://img.shields.io/docker/build/djbrown/riddlebase.svg)](https://hub.docker.com/r/djbrown/riddlebase/builds/)
[![Coveralls Coverage Status](https://coveralls.io/repos/github/djbrown/riddlebase/badge.svg)](https://coveralls.io/github/djbrown/riddlebase)
[![Codecov Coverage Status](https://codecov.io/github/djbrown/riddlebase/coverage.svg)](http://codecov.io/github/djbrown/risslebase/)
[![Codacy Quality Badge](https://api.codacy.com/project/badge/Grade/9c0920594c0544d9b63caf9fab3970d8)](https://www.codacy.com/app/djbrown/riddlebase?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=djbrown/riddlebase&amp;utm_campaign=Badge_Grade)
[![Mypy Badge](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Sauce Test Status](https://saucelabs.com/buildstatus/djbrown-riddlebase)](https://saucelabs.com/u/djbrown-riddlebase)
[![FOSSA License Status](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdjbrown%2Friddlebase.svg?type=shield)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdjbrown%2Friddlebase?ref=badge_shield)

[![Sauce Labs Browsers](https://saucelabs.com/browser-matrix/djbrown-riddlebase.svg)](https://saucelabs.com/u/djbrown-riddlebase)

This is a Web Platform for logic puzzle games

RiddleBase is powered by Django

[<img src="https://www.djangoproject.com/m/img/logos/django-logo-positive.svg" height="50" alt="Django Logo"/>](https://www.djangoproject.com/)


## Running via Docker

`docker run -p 8001:8000 djbrown/riddlebase`<br/>
Container is reachable under [0.0.0.0:8001](http://0.0.0.0:8001)


## Running natively

### Requirements
1. Python 3.7
2. pipenv (`pip install pipenv`)


### Installation
`pipenv install`<br/>
`pipenv run python manage.py migrate`

### Start Application
`pipenv run python manage.py runserver`


## Main Management Commands

* **setup**: fetch associations, districts, seasons and leagues
* **import_games**: fetch games and sport halls
* **import_scores**: fetch players and scores

Execute Commands via `pipenv run python manage.py <COMMAD> <OPTIONS>`.<br/>
Prepend `docker run <CONTAINER> ` when running via Docker.<br/>
Append ` -h` to display Command help.


## License

The project is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).

[![FOSSA License Report](https://app.fossa.io/api/projects/git%2Bgithub.com%2Fdjbrown%2Friddlebase.svg?type=large)](https://app.fossa.io/projects/git%2Bgithub.com%2Fdjbrown%2Friddlebase?ref=badge_large)


## Contributing
See [CONTRIBUTING.md](.github/CONTRIBUTING.md)
