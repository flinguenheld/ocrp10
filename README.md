![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=10&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=In&nbsp;progress&color=green&style=for-the-badge)

# ocrp10

Créez une API sécurisée RESTful en utilisant Django REST

![Logo LITReview](https://raw.githubusercontent.com/FLinguenheld/ocrp10/main/logos/softdesk.png "Logo")

****
### Description
The project purpose is to discover Django REST framework, thanks to the development of backend application.
This application is an issue tracking system and it need an API.
The latter allows to:
- Create an account and login
- Create projects
- Associate users to projects
- Create issues for a project (associated with users)
- Create comments for these issues

****
### Documentations


****
### Installation

Open your terminal and move to the folder where you want to install the API.  
Then, clone this depot :

    git clone https://github.com/FLinguenheld/ocrp10

Move into the *ocrp10/* folder and create a virtual environment :

    python -m venv env

Active it :

    source env/bin/activate

Necessary packages are listed in the file *requirement.txt*.  
Install them :

    pip install -r requirement.txt

****
### Launch

Move to the *ocrp10/* folder and activate the virtual environment.
Launch the server with the command :

    python manage.py runserver

* The terminal will display all requests, you can stop it with **Ctrl-C***


POSTMAN ?



ADMIN ?




****
### Comptes

    admin@softdesk.fr
    admin37

    flo@softdesk.fr
    softdesk2000

    gerard@softdeskfr
    softdesk2000

****
### Pep8

The flake8 package is present in the virtual environment. You can generate a new report with the following command :
(check the folder *flake8-report/* to see results)

    flake8
