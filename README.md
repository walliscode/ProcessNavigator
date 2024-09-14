# ProcessNavigator


## First time operations/updating operations
1. update packages
    - run ```pip install -r .\requirements.txt```
    - equally to update requirements just run ```pip freeze > .\requirements.txt```

## Running the app
1. open up virtual environment with ```.\.venv\Scripts\activate``` in the terminal
2. type and run ```flask --app .\process_navigator\ run --debug``` in the terminal

## formatting
There is package called ```black``` installed which can be run from terminal ```black _directory_``` and it will automatically format your files to a pep8 standard