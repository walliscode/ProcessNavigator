from tests.utils import provide_stacked_response
from process_navigator.extensions.database import db
from process_navigator.models.process import ProcessMethod
from process_navigator.models.analysis import AnalysisMethod


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


def test_edit_analysis_method_post_delete_method_part(client, route_options, test_app):
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
