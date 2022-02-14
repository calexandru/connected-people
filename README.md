# ConnectionApp Api



## Description

ConnectionApp Api - REST API which will return whether two “developers” are fully connected or not.
Given a pair of developer handles they are considered connected if:

* They follow each other on Twitter.
* They have at least a Github organization in common..

## Local development

The api setup uses Docker to build an image and then running that as a Docker container
(Pycharm / VSCode or other IDEs can be setup to use the Python interpreter from the docker image).
For a more lightweight local development it is recommended to use poetry
and python virtual environment.

### Install poetry

* ``curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python``
Install Poetry if you don't have it already (https://python-poetry.org/docs/#installation)

> note::
Ensure you add the following to your system PATH: *$HOME/.poetry/bin* (usually in ~/.bashrc or ~/.zshrc)

* ``poetry --version`` Check install

### Using local installed Python 3.8+

* ``poetry env use /usr/bin/python3``
* ``poetry install`` Install project dependencies (if it fails, try running ``poetry lock`` first)
* ``poetry run which python`` This will point you to the Python interpreter used by Poetry (you can set that in your IDE and start coding)

### Using pyenv

* ``curl https://pyenv.run | bash`` Install pyenv if you don't have it already (https://github.com/pyenv/pyenv)

> note:: If you are using zsh execute the script above using zsh rather than bash
> note:: Run ``pyenv init`` and follow the instructions to enable pyenv in your terminal

* ``pyenv install 3.8.10 -s`` Ensure Python 3.8+ is available in the Pyenv versions
* ``cd`` into your local project directory
* ``pyenv local 3.8.10`` Activate Python 3.8+ for the current project (each time you cd to the project the default Python interpreter will be python3.9)
* ``poetry install`` Install project dependencies (if it fails, try running ``poetry lock`` first)
* ``poetry run which python`` This will point you to the Python interpreter used by Poetry (you can set that in your IDE and start coding)

### Using virtualenv

> note:: You need to have Python 3.9 installed and accessible in your PATH

* ``python3 -m venv app-venv`` Create a new Python virtual environment
* ``source app-venv/bin/activate`` Activate the Python 3.8+ virtual environment
* ``poetry install`` Install project dependencies (if it fails, try running ``poetry lock`` first)
* ``poetry run which python`` This will point you to the Python interpreter used by Poetry (you can set that in your IDE and start coding)

## Install Git pre-commit hooks

For a clean development and to ensure the quality of the code commits it is highly recommended to install

> note:: there should be an existent Git repository - ``git init``

``poetry run pre-commit install`` This will add git pre commit hooks

## Test application

``poetry run pytest`` (run existing test suite).

## Run code style checks

``poetry run pre-commit run --all-files``

## Run the api's Docker image locally

Typically, one would release the api and would run the Docker image generated via the build system.

To build an image from the codebase:

``docker build -t connection_api:latest .``

To start dependency services (mongo):

``docker-compose up -d``

To run the image use:

``docker run -p 5000:5000 -e MONGO_HOST=<mongo ip> -e TWITTER_ACCESS_TOKEN=<token> connection_api:latest``

## Test cases

For connected users call the api with the following handles:

http://localhost:5000/connected/realtime/dstufft/gvanrossum

For users that are not connected call the api with the following handles:

http://localhost:5000/connected/realtime/calexandru/gvanrossum

To see history of the api call:

http://localhost:5000/connected/register/dstufftss/gvanrossum

## Release

Below are instructions on how to trigger a new release.

> note:: TODO
