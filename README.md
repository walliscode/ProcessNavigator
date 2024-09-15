# ProcessNavigator


## First time operations/updating operations
1. update packages
    - run ```pip install -r .\requirements.txt```
    - equally to update requirements just run ```pip freeze > .\requirements.txt```

2. create database 
    - create the instance folder in the root directory (next to the process_navigator folder)
    - if the database doesn't exist then it needs to be created via the python shell. If you run ``flask --app .\process_navigator\ shell``` in the terminal you will enter a python shell with app context. this allows you to perform database operations
    - when in the shell run ```db.create_all()``` and the database will be created in the instance folder.
    - ```ctrl-z``` to exit
    - n.b. running ```db.drop_all() will clear the database file of all data and models. use wisely

## Running the app
1. open up virtual environment with ```.\.venv\Scripts\activate``` in the terminal
2. type and run ```flask --app .\process_navigator\ run --debug``` in the terminal

## instance folder
The instance folder is in the gitignore folder. So, this is where to store anything specific to this instance of the app, such as databases, config e.t.c.

You could also use this to run the app with multiple databases depending on what arguments you pass to the flask cli.

## formatting
There is package called ```black``` installed which can be run from terminal ```black _directory_``` and it will automatically format your files to a pep8 standard


