A simple app which subscribes to the coinbase feed and streams volume-weighted average prices for the pairs of choice.

To make sure it works, install the requirements, run

`python -m app.main.py`

and check out the stdout.

In your IDE of choice you can run the test suites, or use pytest directly.

Here I assume you use Pipenv for package management (see
https://pipenv-fork.readthedocs.io/en/latest/install.html for installation instructions)

As a fallback, there's a pipenv-generated requirements.txt,
but I encourage you to try Pipenv (unless you don't develop libraries which
should support several Python versions): using

`pipenv run $scriptname`

you can do many useful things: see the list of commands in the Pipfile's [scripts] section.

In case you don't have the most recent Python installed, I recommend asdf
(see https://asdf-vm.com/guide/getting-started.html#_1-install-dependencies for instructions).

Generaly pipenv and asdf get along well, but keep in mind that their integration can be tedious in some cases.
