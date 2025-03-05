from tests.utils import provide_stacked_response
from process_navigator.extensions.database import db
from process_navigator.models.process import Process


def test_cauldron_index_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "cauldron_index_get"]

    # get the response

    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/cauldron/"
    html_data = [
        "Welcome to the Cauldron, this is the kick off point for setting up Process(es) and commiting them to the database",
    ]

    for data in html_data:
        assert data.encode() in response.data


# show that the user cannot access the process_path page directly
def test_cauldron_process_path_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_process_path_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/cauldron/"


def test_cauldron_index_post_start(client, route_options):
    #    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_post_start",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/cauldron/process_path"


def test_cauldron_process_path_get_success(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_post_start",
        "cauldron_process_path_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/cauldron/process_path"


def test_cauldron_process_path_commit_path_one(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_post_start",
        "cauldron_process_path_get",
        "cauldron_process_path_commit_path_one",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200

    # check for database entries
    with test_app.app_context():
        process_query = db.session.execute(db.select(Process)).scalars().all()
        assert len(process_query) == 1
        process = process_query[0]
        assert process.process_date.strftime("%Y-%m-%d") == "2020-01-01"

        # check for Process Steps
        assert len(process.process_steps) == 1

        # check indivual Process Steps
        process_step_one = process.process_steps[0]
        assert process_step_one.order == 1
        assert process_step_one.process_method_part_id == 1
        assert process_step_one.process_id == 1

        # check for Step parameters
        process_step_one_parameters = process_step_one.step_params
        assert len(process_step_one_parameters) == 1
        assert process_step_one_parameters[0].value == 6.7
        assert process_step_one_parameters[0].param_id == 1
        assert process_step_one_parameters[0].process_step_id == 1

        # check for Step Inputs
        process_step_one_inputs = process_step_one.step_inputs
        assert len(process_step_one_inputs) == 1
        assert process_step_one_inputs[0].value == 5.6
        assert process_step_one_inputs[0].input_id == 1
        assert process_step_one_inputs[0].process_step_id == 1


# single path test with two processes with one step each
def test_cauldron_process_path_commit_path_two(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_post_start",
        "cauldron_process_path_get",
        "cauldron_process_path_commit_path_two",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    # check for database entries
    with test_app.app_context():
        process_query = db.session.execute(db.select(Process)).scalars().all()
        assert len(process_query) == 2
        process_one = process_query[0]
        assert process_one.process_date.strftime("%Y-%m-%d") == "2020-01-01"
        # check for Process Steps
        assert len(process_one.process_steps) == 1
        # check indivual Process Steps
        process_one_step_one = process_one.process_steps[0]
        assert process_one_step_one.order == 1
        assert process_one_step_one.process_method_part_id == 1
        assert process_one_step_one.process_id == 1

        # check for Step parameters
        process_one_step_one_parameters = process_one_step_one.step_params
        assert len(process_one_step_one_parameters) == 1
        assert process_one_step_one_parameters[0].value == 6.7
        assert process_one_step_one_parameters[0].param_id == 1
        assert process_one_step_one_parameters[0].process_step_id == 1

        # check for Step Inputs
        process_one_step_one_inputs = process_one_step_one.step_inputs
        assert len(process_one_step_one_inputs) == 1
        assert process_one_step_one_inputs[0].value == 5.6
        assert process_one_step_one_inputs[0].input_id == 1

        process_two = process_query[1]
        assert process_two.process_date.strftime("%Y-%m-%d") == "2020-01-02"
        # check for Process Steps
        assert len(process_two.process_steps) == 1
        # check indivual Process Steps
        process_two_step_one = process_two.process_steps[0]
        assert process_two_step_one.order == 1
        assert process_two_step_one.process_method_part_id == 1
        assert process_two_step_one.process_id == 2

        # check for Step parameters
        process_two_step_one_parameters = process_two_step_one.step_params
        assert len(process_two_step_one_parameters) == 1
        assert process_two_step_one_parameters[0].value == 3.45
        assert process_two_step_one_parameters[0].param_id == 1
        assert process_two_step_one_parameters[0].process_step_id == 2

        # check for Step Inputs
        process_two_step_one_inputs = process_two_step_one.step_inputs
        assert len(process_two_step_one_inputs) == 1
        assert process_two_step_one_inputs[0].value == 2.34
        assert process_two_step_one_inputs[0].input_id == 1
        assert process_two_step_one_inputs[0].process_step_id == 2


def test_cauldron_process_path_commit_path_three(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "cauldron_index_post_start",
        "cauldron_process_path_get",
        "cauldron_process_path_commit_path_three",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    # check for database entries
    with test_app.app_context():
        process_query = db.session.execute(db.select(Process)).scalars().all()
        assert len(process_query) == 3
        process_one = process_query[0]
        assert process_one.process_date.strftime("%Y-%m-%d") == "2020-01-01"
        # check for Process Steps
        assert len(process_one.process_steps) == 1
        # check indivual Process Steps
        process_one_step_one = process_one.process_steps[0]
        assert process_one_step_one.order == 1
        assert process_one_step_one.process_method_part_id == 1
        assert process_one_step_one.process_id == 1
        # check for Step parameters
        process_one_step_one_parameters = process_one_step_one.step_params
        assert len(process_one_step_one_parameters) == 1
        assert process_one_step_one_parameters[0].value == 6.7
        assert process_one_step_one_parameters[0].param_id == 1
        assert process_one_step_one_parameters[0].process_step_id == 1
        # check for Step Inputs
        process_one_step_one_inputs = process_one_step_one.step_inputs
        assert len(process_one_step_one_inputs) == 1
        assert process_one_step_one_inputs[0].value == 5.6
        assert process_one_step_one_inputs[0].input_id == 1

        # Process Two
        process_two = process_query[1]
        assert process_two.process_date.strftime("%Y-%m-%d") == "2020-01-01"
        # check for Process Steps
        assert len(process_two.process_steps) == 1
        # check indivual Process Steps
        process_two_step_one = process_two.process_steps[0]
        assert process_two_step_one.order == 1
        assert process_two_step_one.process_method_part_id == 1
        assert process_two_step_one.process_id == 2
        # check for Step parameters
        process_two_step_one_parameters = process_two_step_one.step_params
        assert len(process_two_step_one_parameters) == 1
        assert process_two_step_one_parameters[0].value == 1
        assert process_two_step_one_parameters[0].param_id == 1
        assert process_two_step_one_parameters[0].process_step_id == 2
