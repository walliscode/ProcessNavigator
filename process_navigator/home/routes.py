import eralchemy2

# import flask functionality
from flask import current_app, flash, redirect, render_template, session, url_for

from process_navigator.extensions import db
from process_navigator.home import bp
from process_navigator.models.admin import User
from process_navigator.utils.decorators import login_required, session_keys

from .forms import LoginForm, RegistrationForm


@bp.route("/")
@login_required
@session_keys()
def index():
    return render_template("home/index.html")


# add registration route to add new user to User table
@bp.route("/register", methods=["GET", "POST"])
@session_keys()
def register():
    form = RegistrationForm()
    if form.submit.data:
        # first check if user email already exists
        email_check = db.session.execute(
            db.select(User).filter(User.email == form.email.data)
        ).scalar()
        # if email already exists, flash message and return to registration page
        if email_check is not None:
            flash(
                "User with email {email} already exists.".format(email=form.email.data),
                "error-message",
            )
            return render_template("home/register.html", form=form)

        # if email does not exist, add user to the Database
        new_user = User(
            first_name=form.first_name.data.__str__(),
            last_name=form.last_name.data,
            email=form.email.data,
            password=form.password.data,
        )

        db.session.add(new_user)
        db.session.commit()

        # check if user was added to the Database
        user_check = db.session.execute(
            db.select(User).filter(User.email == form.email.data)
        ).scalar()
        if user_check is not None:
            message = "User {first_name} {last_name} was registered successfully with email {email}.".format(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
            )
            flash(message, "success-message")
        else:
            message = "User {first_name} {last_name} was not registered.".format(
                first_name=form.first_name.data, last_name=form.last_name.data
            )
            flash(message, "error-message")

    return render_template("home/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
@session_keys()
def login():
    form = LoginForm()

    if form.submit.data:
        # check if user email exists
        user = db.session.execute(
            db.select(User).filter(User.email == form.email.data)
        ).scalar()

        # if user does not exist, flash message and return to login page
        if user is None:
            flash(
                "User with email {email} does not exist.".format(email=form.email.data),
                "error-message",
            )
            return render_template("home/login.html", form=form)

        # if user exists, check if password is correct
        if user.password == form.password.data:
            if "security_keys" not in session:
                session["security_keys"] = []

            session["security_keys"].append("user")
            session["user"] = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "id": user.id,
            }

            return redirect(url_for("home.index"))

        else:
            flash(
                "Incorrect password for user {email}.".format(email=form.email.data),
                "error-message",
            )

    return render_template("home/login.html", form=form)


@bp.route("/erdiagram")
def erdiagram():
    try:
        db_path = "postgresql://postgres:test@localhost/processnavigator"
        output_path = "process_navigator/static/images/erdiagram.png"

        # Log the paths being used
        current_app.logger.debug(f"Database path: {db_path}")
        current_app.logger.debug(f"Output path: {output_path}")

        # Render the ER diagram
        eralchemy2.render_er(db_path, output_path)

        # Log success
        current_app.logger.debug("ER diagram rendered successfully.")

    except Exception as e:
        # Log any exceptions with detailed information
        current_app.logger.error(f"Error rendering ER diagram: {e}", exc_info=True)
        return "An error occurred while generating the ER diagram.", 500

    return render_template("home/erdiagram.html")
