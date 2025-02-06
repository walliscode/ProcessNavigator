from tests.utils import provide_stacked_response


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
