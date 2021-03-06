# CCE Search Prototype

An unofficial, experimental interface to search records digitized by NYPL's
[Catalog of Copyright Entries project](https://github.com/NYPL/catalog_of_copyright_entries_project).

Forked from Sean Redmond's [original protype](https://github.com/seanredmond/cce-search-prototype).

## Required software

- Python 3.7
- Pipenv

### Why Pipenv?

Using a virtual environment is very important for ensuring that all work is done in a standardized Python environment. In order to simplify using a virtual environment as well as to give us the ability to create deterministic builds, we use [Pipenv](https://realpython.com/pipenv-guide/).

## Installing Pipenv

### Mac

`brew install pipenv`

*Note: Mac users can also install through Pip, but using Homebrew is recommended.*

### Other systems

`pip install --user pipenv`

*Note: You may have versions of Pip installed for both Python 2 and 3. If so, your Python 3 Pip will be called pip3. Check if this is the case by running `pip --version` and `pip3 --version`.*

## Installing all dependencies and creating the virtual environment

Run `pipenv install` in the project's main directory. If installing for development purposes, rather than deployment, add the `--dev` flag to install required development packages as well.

## Installing new packages

In the project directory, use `pipenv install` the same way you would use `pip install`. The package will be installed in the virtual environment, and the Pipfile will be updated.

For example, to install the package requests: `pipenv install requests`

To specify a specific package version: `pipenv install flask==0.12.1`

To install packages for development purposes (e.g. ones that aren't required to build and run the project, but are useful for working on it), you can use the --dev flag. For example, `pipenv install pytest --dev`. 

## Activating the virtual environment

To activate the virtual environment in your current shell, run `pipenv shell`. The virtual environment will be indicated by a change to your terminal prompt.

## "Locking" the virtual environment

To ensure a deterministic build and "lock" the versions of packages and their subdependencies, run `pipenv lock`. This will ensure Pipfile.lock is up to date. Do this when you intend to push any changes to the production environment.

## Remove an unneeded package

To remove a package from the Pipfile and uninstall it from your virtual environment, use `pipenv uninstall`.

For example, to remove beautifulsoup: `pipenv uninstall beautifulsoup`

## Run a single command in the virtual environment without activating it

`$ pipenv run [command_goes_here]`

## Closing the virtual environment

After you have activated the virtual environment, press `ctrl-d` to exit. Your terminal prompt should return to its original appearance.

**Always do this when you're finished working in the virtual environment, otherwise your other Python work will screw up the project!**

## Deploying the project locally

After activating the virtual environment, run `flask run` within the root directory of the project:

The Flask app will then be running at [localhost:5000](localhost:5000).

Optionally, use `export FLASK_ENV=development` before running the app to enable useful debugging tools.

To close the application, end the process with `ctrl-c` in your terminal. 

## Running Tests

In the root directory of the project, run 

`python -m pytest`. 

This will run the entire test suite. New test functions and files must be contained in the `tests/` directory.

To see test coverage data, run `python -m pytest --cov`. To generate an HTML coverage report, run `python -m pytest --cov-report html tests/ --cov=./`. Then, run `python -m http.server` and navigate to [localhost:8000](localhost:8000) to view it.

## Troubleshooting

    The 'pipenv==20XX.XX.XX' distribution was not found and is required by the application

Reinstall Pipenv, with the methods specified [above](#Installing-Pipenv).

    Warning: Your Pipfile requires python_version 3.7, but you are using X.X.X (/Users/...).
    $ pipenv check will surely fail.

This means your Python installation has changed since you first created the venv with `pipenv install`. Delete it using `pipenv --rm`, then [rebuild it](#Installing-all-dependencies-and-creating-the-virtual-environment).