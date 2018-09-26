=========
Projector
=========

Projector is a tool for managing repositories and setting up development
environments.

Development
===========

|pipenv|_ is recommended for devlopment. Run the following to set up a development environment::

    pipenv install --dev

This will create the virtual environment and install all required development
packages. See the |pipenv|_ documentation or run ``pipenv --help`` for more
information on working with |pipenv|_.


Building Documentation
----------------------

The documentation can be built locally using the following command::

    python setup.py sphinx_build

The generated HTML documentation will be placed in ``build/sphinx/html``.


.. |pipenv| replace:: ``pipenv``
.. _pipenv: https://docs.pipenv.org
