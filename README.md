###### DESCRIPTION
A websocket client which subscribes to the coinbase feed and streams volume-weighted average prices for the pairs of choice.

###### LAUNCH

To start the client, install the requirements with pipenv or pip, run

`pipenv run app`

or

`python -m app.main.py`

and see resulting averages streamed in stdout.

###### PIPENV SCRIPTS
Here I assume you use Pipenv for package management (see
https://pipenv-fork.readthedocs.io/en/latest/install.html for installation instructions)

As a fallback, there's a pipenv-generated *requirements.txt*,
but I encourage you to try Pipenv (unless you don't develop libraries which
should support several Python versions).

In case you don't have the required Python version, I recommend installing it via asdf
(see https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies for instructions).

Generaly pipenv and asdf get along well, but keep in mind that their integration can be tedious in some cases.


Here are some pipenv scripts used in the project:

`pipenv run app` - starts the application

`pipenv run tests` - run test cases

For contributions, the following scripts can be used:

`pipenv run add-hooks` - install pre-commit hooks

`pipenv run remove-hooks` - uninstall them

`pipenv run check-types` - make sure all types are set

`pipenv run check-flake8` - run flake8
