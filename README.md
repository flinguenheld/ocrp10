![badge](https://img.shields.io/static/v1?label=Project&nbsp;OC&message=10&color=blueviolet&style=for-the-badge)
![badge](https://img.shields.io/static/v1?label=Status&message=In&nbsp;progress&color=green&style=for-the-badge)

# ocrp10

Create a Secure RESTful API Using Django REST

![Logo LITReview](https://raw.githubusercontent.com/FLinguenheld/ocrp10/main/logos/softdesk.png "Logo")

****
### Description
The project purpose is to discover Django REST framework thanks to the development of a backend application.
This application is an issue tracking system and needs an API.
The latter allows to:
- Create accounts and login
- Create projects
- Associate users to projects
- Create issues for a project (associated with users)
- Create comments for these issues

All actions are secure according to the [documentation](#documentation).

****
### Installation

Open your terminal and move to the folder where you want to install the API.  
Then, clone this depot :

    git clone https://github.com/FLinguenheld/ocrp10

Move into *ocrp10/* folder and create a virtual environment :

    python -m venv env

Active it :

    source env/bin/activate

Necessary packages are listed in the file *requirement.txt*.  
Install them :

    pip install -r requirement.txt

****
### Launch

Move into *ocrp10/* folder and activate the virtual environment.
Launch the server with the command :

    python manage.py runserver

* The terminal will display all requests, you can stop it with **Ctrl-C***

Then, you can use your browser, Postman or your terminal as well.

    http://localhost:8000/

****
### Documentations

<a name='documentation'></a>
All endpoints are explain in the Postman documentation :

[![Logo PostMan](https://raw.githubusercontent.com/FLinguenheld/ocrp10/main/logos/postman.png "Postman")](https://documenter.getpostman.com/view/19051270/UzQvtQt1)

****
### Tests

To easily test this API, the SQLite file is present in this repository.  
It already contains several users :


    admin@softdesk.fr       admin37

    flo@softdesk.fr         softdesk2000
    gerard@softdesk.fr      softdesk2000
    michel@softdesk.fr      softdesk2000

Moreover, the admin website is open, you can access by this url and use the admin account :

    http://localhost:8000/admin/

****
### Pep8

The flake8 package is present in the virtual environment. You can generate a new report with the following command :  
(check the folder *flake8-report/* to see results, and the file *tox.ini* to modify options)

    flake8
