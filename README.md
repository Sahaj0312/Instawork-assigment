# Introduction

This is a simple django application that allows a user to keep track of members in a team.

# Usage

This assumes that `python3` is linked to valid installation of python 3 and that `pip` is installed and `pip3`is valid for installing python 3 packages.

First, clone the repository and navigate to the Instawork-assigment project:

    $ git clone https://github.com/Sahaj0312/Instawork-assigment.git
    $ cd Instawork-assigment

Then, install all the requirements:

    $ pip3 install -r requirements.txt

Then, apply the migrations:

    $ python3 manage.py migrate 

And then, start the development server:

    $ python3 manage.py runserver

# Testing

This repository includes unit and functional tests (using Selenium).

Run the tests by executing the following command in a new terminal:

    $ python3 manage.py test base
