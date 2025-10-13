# ProcessNavigator


## First time operations/updating operations
1. update packages
    - run ```pip install -r .\requirements.txt```
    - equally to update requirements just run ```pip freeze > .\requirements.txt```

### Database set up
1. This flask is designed around using a POSTGRESQL database. however altering the SQLALCHEMY_DATABASE_URI in the __init__.py file will allow you to use other DBMS.
2. Install postgresql from the [official website](https://www.postgresql.org/download/) and set your password during installation.
3. Add the postgres bin folder to the environment variables.
4. Next open a termainal and type ```psql -U postgres``` to open the postgres shell. This is the superuser default for postgres and should use your password you set up during installation.

5. Create a database by typing ```CREATE DATABASE processnavigator;``` in the shell. This will create a database called processnavigator.
6. Create a user by typing ```CREATE USER processnavigator WITH PASSWORD 'test';``` in the shell. This will create a user called processnavigator with the password 'test'.
7. Change the ownership of the database to the user by typing ```ALTER DATABASE processnavigator OWNER TO processnavigator;``` in the shell. This should grant the user full access to the database.
8. Exit the shell by typing ```\q```.

9. Now we need to create the tables from the schema in the python shell. To do this open a terminal and type ```flask --app process_navigator shell```. This will open the python shell with the app context.

10. Now type the following commands in the shell to create the tables:
    ```python
    db.create_all()
    ```

11. Now you should have a database with the tables created.
12. Exit the shell by typing ```exit()```.
13. This should be one time setup. Any commands such as ```db.drop_all()``` will drop all the tables in the database and remove all data. HANDLE WITH CARE.

## Running the app
1. open up virtual environment with ```.\.venv\Scripts\activate``` in the terminal
2. type and run ```flask --app .\process_navigator\ run --debug``` in the terminal

## instance folder
The instance folder is in the gitignore folder. So, this is where to store anything specific to this instance of the app, such as databases, config e.t.c.

You could also use this to run the app with multiple databases depending on what arguments you pass to the flask cli.

## formatting
There is package called ```black``` installed which can be run from terminal ```black _directory_``` and it will automatically format your files to a pep8 standard

## Future Features
- Database diagram visualization will be added at a later stage of the project


