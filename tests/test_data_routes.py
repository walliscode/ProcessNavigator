from tests.utils import provide_stacked_response
from process_navigator.extensions.database import db
from process_navigator.models.process import ProcessMethod
from process_navigator.models.analysis import AnalysisMethod
from process_navigator.models.parameters import Param
from process_navigator.models.inputs import Input


# user attempts to access data page without being logged in
def test_data_index_get_fail(client, route_options):
    # set up paths for this test to follow
    paths = ["data_index_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/login"


# user attempts to access data page after logging in
def test_data_index_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "data_index_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Data"]
    for data in html_data:
        assert data.encode() in response.data


# user navigates to process method page via the data index page
def test_process_method_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Process Methods",
        "Welcome to the Process Methods page",
        "Add Method",
        "Edit Method",
        "Delete Method",
    ]
    for data in html_data:
        assert data.encode() in response.data


# user navigates to add process method page via the process method page
def test_process_method_post_add_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_add_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302


# user gets the add process method page via the process method page
def test_add_process_method_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_add_method",
        "add_process_method_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Add Process Method",
        "Name",
        "Description",
        "Add Method",
    ]
    for data in html_data:
        assert data.encode() in response.data


def test_process_method_post_delete_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_delete_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/delete_process_method"


# user navigates to the delete process method page via the process method page
def test_delete_process_method_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_delete_method",
        "delete_process_method_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Delete Process Method",
        "Delete Method",
    ]
    for data in html_data:
        assert data.encode() in response.data


def test_delete_process_method_delete_method(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "process_method_get",
        "process_method_post_delete_method",
        "delete_process_method_get",
        "delete_process_method_post",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/process_methods"

    html_data = [
        "Process Method test_process_method_1 and Process Method Parts test_part_1, test_part_2, test_part_3 deleted from database"
    ]
    for data in html_data:
        assert data.encode() in response.data

    # check in database
    with test_app.app_context():
        process_method_query = db.session.execute(
            db.select(ProcessMethod).filter(
                ProcessMethod.name == "test_process_method_1"
            )
        ).scalar_one_or_none()

        assert process_method_query is None


# user navigates to the units page via the data index page
def test_units_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "data_index_get", "units_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Units",
        "Welcome to the Units page",
        "Add Unit",
        "Edit Unit",
        "Delete Unit",
    ]
    for data in html_data:
        assert data.encode() in response.data


# user navigates to the analysis methods page via the data index page
def test_analysis_methods_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "data_index_get", "analysis_methods_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/analysis_methods"
    html_data = [
        "Analysis Methods",
        "Welcome to the Analysis Methods page",
        "Add Analysis Method",
        "Edit Analysis Method",
        "Delete Analysis Method",
    ]
    for data in html_data:
        assert data.encode() in response.data


# "User navigates to the add analysis method page via the analysis methods page"
def test_analysis_methods_post_add_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_add_analysis_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/add_analysis_method"


# "user gets the add analysis method page via the analysis methods page"
def test_add_analysis_method_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_add_analysis_method",
        "add_analysis_method_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Add Analysis Method",
        "Name",
        "Description",
        "Add Method",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User adds an analysis method
def test_add_analysis_method_post(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_add_analysis_method",
        "add_analysis_method_get",
        "add_analysis_method_post_add_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/analysis_methods"

    with test_app.app_context():
        analysis_method_query = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.name == "test_analysis_method_2"
            )
        ).scalar_one_or_none()

        assert analysis_method_query is not None
        assert len(analysis_method_query.analysis_method_parts) == 3
    html_data = ["Analysis Method test_analysis_method_2"]
    for data in html_data:
        assert data.encode() in response.data


# User navigates to the edit analysis method page via the analysis methods page
def test_analysis_methods_post_edit_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/edit_analysis_method"


# user selects an analysis method to edit
def test_edit_analysis_method_post_select_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
        "edit_analysis_method_post_select_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200

    html_data = [
        "Method Name",
        "test_analysis_method_1",
        "Method Description",
        "test_description",
        "Method File",
        "Method Part Name",
        "Data Type",
        "Unit",
        "Continuous",
        "Categorical",
        "String",
    ]

    for data in html_data:
        assert data.encode() in response.data


# User adds another method part option to the form
def test_edit_analysis_method_post_add_method_part(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
        "edit_analysis_method_post_select_method",
        "edit_analysis_method_post_add_method_part",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = [
        "Method Name",
        "test_analysis_method_1",
        "Method Description",
        "test_description",
        "Method File",
        "Method Part Name",
        "Data Type",
        "Unit",
        "Continuous",
        "Categorical",
        "String",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User commits changes to the analysis method
def test_edit_analysis_method_post_commit_changes_1(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
        "edit_analysis_method_post_select_method",
        "edit_analysis_method_post_add_method_part",
        "edit_analysis_method_post_commit_changes_1",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/analysis_methods"
    with test_app.app_context():
        analysis_method_query = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.name == "test_analysis_method_1"
            )
        ).scalar_one_or_none()
        assert analysis_method_query is not None
        assert len(analysis_method_query.analysis_method_parts) == 4
    html_data = [
        "Analysis Method test_analysis_method_1 and Analysis Method Parts test_part_1, test_part_2, test_part_3, test_part_4 updated in database"
    ]
    for data in html_data:
        assert data.encode() in response.data


# User deletes a method part from the analysis method (without commiting changes)


def test_edit_analysis_method_post_delete_method_part(
    client,
    route_options,
):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
        "edit_analysis_method_post_select_method",
        "edit_analysis_method_post_delete_method_part",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200


# User deletes a method part from the analysis method (and commits changes)
def test_edit_analysis_method_post_commit_changes_2(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_edit_analysis_method",
        "edit_analysis_method_post_select_method",
        "edit_analysis_method_post_delete_method_part",
        "edit_analysis_method_post_commit_changes_2",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/analysis_methods"
    with test_app.app_context():
        analysis_method_query = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.name == "test_analysis_method_1"
            )
        ).scalar_one_or_none()
        assert analysis_method_query is not None
        assert len(analysis_method_query.analysis_method_parts) == 2
    html_data = [
        "Analysis Method test_analysis_method_1 and Analysis Method Parts test_part_1, test_part_2 updated in database"
    ]
    for data in html_data:
        assert data.encode() in response.data


# User redirects to the delete analysis method page via the analysis methods page
def test_analysis_methods_post_delete_method(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_delete_analysis_method",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/delete_analysis_method"


# User navigates to the delete analysis method page via the analysis methods page
def test_delete_analysis_method_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_delete_analysis_method",
        "delete_analysis_method_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Delete Analysis Method"]
    for data in html_data:
        assert data.encode() in response.data


# User deletes an analysis methods
def test_delete_analysis_method_post_analysis_method(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "analysis_methods_get",
        "analysis_methods_post_delete_analysis_method",
        "delete_analysis_method_get",
        "delete_analysis_method_post",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/analysis_methods"
    html_data = [
        "Analysis Method test_analysis_method_1 and Analysis Method Parts test_part_1, test_part_2, test_part_3 deleted from database"
    ]
    for data in html_data:
        assert data.encode() in response.data
    # check in database
    with test_app.app_context():
        analysis_method_query = db.session.execute(
            db.select(AnalysisMethod).filter(
                AnalysisMethod.name == "test_analysis_method_1"
            )
        ).scalar_one_or_none()
        assert analysis_method_query is None


# User navigates to the parameters page via the data index page
def test_parameters_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "data_index_get", "parameters_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/parameters"
    html_data = [
        "Parameters",
        "Welcome to the Parameters page",
        "Add Parameter",
        "Edit Parameter",
        "Delete Parameter",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User folows parameters route to add_parameters via add_parameter button
def test_add_parameters_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_add_parameter",
        "add_parameter_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200


# User adds a duplicate parameter and gets feedback message
def test_add_parameters_post_add_duplicate_parameter(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_add_parameter",
        "add_parameter_get",
        "add_parameter_post_add_duplicate_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/add_parameter"
    html_data = [
        "Parameter test_parameter_1 already exists in the database",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User adds a parameter to the database
def test_add_parameters_post_add_parameter(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_add_parameter",
        "add_parameter_get",
        "add_parameter_post_add_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/parameters"
    with test_app.app_context():
        parameter_query = db.session.execute(
            db.select(Param).filter(Param.name == "test_parameter_3")
        ).scalar_one_or_none()
        assert parameter_query is not None
    html_data = [
        "Parameter test_parameter_3 added to database",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User navigates to the edit paramerer route from the parameters page
def test_parameters_post_edit_parameter(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_edit_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/edit_parameter"


# User navigates to the edit parameter page via the parameters page
def test_edit_parameter_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_edit_parameter",
        "edit_parameter_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Edit Parameters", "Select Parameter"]
    for data in html_data:
        assert data.encode() in response.data


# User selects a parameter to edit
def test_edit_parameter_post_select_parameter(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_edit_parameter",
        "edit_parameter_get",
        "edit_parameter_post_select_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/edit_parameter"
    html_data = [
        "Parameter Name",
        "test_parameter_1",
        "Unit Velocity",
        "Kms^-1",
        "Commit Changes",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User commits parameter Changes
def test_edit_parameter_post_commit_changes(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_edit_parameter",
        "edit_parameter_get",
        "edit_parameter_post_select_parameter",
        "edit_parameter_post_commit_changes",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/parameters"
    with test_app.app_context():
        parameter_query = db.session.execute(
            db.select(Param).filter(Param.name == "test_parameter_1")
        ).scalar_one_or_none()
        assert parameter_query is None

        changed_parameter_query = db.session.execute(
            db.select(Param).filter(Param.name == "change_parameter")
        ).scalar_one_or_none()

        assert changed_parameter_query is not None
    html_data = [
        "Parameter change_parameter (Kms^-1) updated in database",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User navigates to the delete parameter route from the parameters page
def test_parameters_post_delete_parameter(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_delete_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/delete_parameter"


# User navigates to the delete parameter page via the parameters page
def test_delete_parameter_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_delete_parameter",
        "delete_parameter_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Delete Parameter"]
    for data in html_data:
        assert data.encode() in response.data


# User deletes a parameter
def test_delete_parameter_post_delete_parameter(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "parameters_get",
        "parameters_post_delete_parameter",
        "delete_parameter_get",
        "delete_parameter_post_delete_parameter",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/parameters"
    html_data = [
        "Parameter test_parameter_1 deleted from database",
    ]
    for data in html_data:
        assert data.encode() in response.data
    # check in database
    with test_app.app_context():
        parameter_query = db.session.execute(
            db.select(Param).filter(Param.name == "test_parameter_1")
        ).scalar_one_or_none()
        assert parameter_query is None


# User navigates to the inputs page via the data index page
def test_inputs_get(client, route_options):
    # set up paths for this test to follow
    paths = ["register_user", "login_user", "data_index_get", "inputs_get"]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/inputs"
    html_data = [
        "Inputs",
        "Welcome to the Inputs page",
        "Add Input",
        "Edit Input",
        "Delete Input",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User navigates to the add input page via the inputs page
def test_add_input_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_add_input",
        "add_input_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/add_input"
    html_data = ["Add Input", "Input Name", "Input CAS", "Unit"]
    for data in html_data:
        assert data.encode() in response.data


# User adds an input to the database
def test_add_input_post_add_input(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_add_input",
        "add_input_get",
        "add_input_post_add_input",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/inputs"
    with test_app.app_context():
        input_query = db.session.execute(
            db.select(Input).filter(Input.name == "test_input_3")
        ).scalar_one_or_none()
        assert input_query is not None
    html_data = [
        "Input test_input_3 (Kms^-1) added to database",
    ]
    for data in html_data:
        assert data.encode()


# User navigates to the edit input route from the inputs page
def test_inputs_post_edit_input(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_edit_input",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/edit_input"


# User navigates to the edit input page via the inputs page
def test_edit_input_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_edit_input",
        "edit_input_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/edit_input"
    html_data = ["Edit Inputs", "Select Input"]
    for data in html_data:
        assert data.encode() in response.data


# User selects an input to edit
def test_edit_input_post_select_input(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_edit_input",
        "edit_input_get",
        "edit_input_post_select_input",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/edit_input"
    html_data = [
        "Input Name",
        "test_input_1",
        "Input CAS",
        "1-2-3-4",
        "Unit Velocity",
        "Kms^-1",
        "Commit Changes",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User commits input changes
def test_edit_input_post_commit_changes(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_edit_input",
        "edit_input_get",
        "edit_input_post_select_input",
        "edit_input_post_commit_changes",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/inputs"
    with test_app.app_context():
        input_query = db.session.execute(
            db.select(Input).filter(Input.name == "test_input_1")
        ).scalar_one_or_none()
        assert input_query is None
        changed_input_query = db.session.execute(
            db.select(Input).filter(Input.name == "change_input")
        ).scalar_one_or_none()
        assert changed_input_query is not None
        assert changed_input_query.CAS == "7-8-9"
    html_data = [
        "Input change_input (Kms^-1) with CAS 7-8-9 updated in database",
    ]
    for data in html_data:
        assert data.encode() in response.data


# User navigates to the delete input route from the inputs page
def test_inputs_post_delete_input(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_delete_input",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 302
    assert response.headers["Location"] == "/data/delete_input"


# User navigates to the delete input page via the inputs page
def test_delete_input_get(client, route_options):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_delete_input",
        "delete_input_get",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    html_data = ["Delete Inputs"]
    for data in html_data:
        assert data.encode() in response.data


# User deletes an input
def test_delete_input_post_delete_input(client, route_options, test_app):
    # set up paths for this test to follow
    paths = [
        "register_user",
        "login_user",
        "data_index_get",
        "inputs_get",
        "inputs_post_delete_input",
        "delete_input_get",
        "delete_input_post_delete_input",
    ]
    # get the response
    response = provide_stacked_response(client, paths, route_options)
    # assert the response status code
    assert response.status_code == 200
    assert response.request.path == "/data/inputs"
    html_data = [
        "Input test_input_1 deleted from database",
    ]
    for data in html_data:
        assert data.encode() in response.data
    # check in database
    with test_app.app_context():
        input_query = db.session.execute(
            db.select(Input).filter(Input.name == "test_input_1")
        ).scalar_one_or_none()
        assert input_query is None
