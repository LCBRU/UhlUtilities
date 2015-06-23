# Python Trials MsSql

## Install

Install a virtual environment

    virtualenv venv
     . venv/bin/activate

Install required libraries

    sudo apt-get install freetds-dev
    sudo apt-get install python-dev
    pip install pymssql

## Setup Environment

Amend the settings in `dbSettings.py`.

## Gotchas

- Servers with an instance must use a double backslash: i.e., server\\\\instance