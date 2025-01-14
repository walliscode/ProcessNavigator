from pathlib import Path

import pytest
from flask import session

from tests.conftest import get_user_paths


@pytest.mark.parametrize("user_path", get_user_paths())
def test_(client, route_options, user_path):
    # first get response object by looping through the user_path path
    response = client.get("/")

    with client:
        for path in user_path["path"]:
            # find the relevenat path in the route_options
            route_info = {}
            for route in route_options:
                if path in route["name"]:
                    route_info = route
                    break

            method = route_info["method"]
            route = route_info["route"]
            data = route_info["data"]

            # if the data requires a file upload then we need to insert it now
            if "file" in data:
                test_files = Path.cwd() / "tests" / "data" / "test_files"

                new_key = data["file"]["field_name"]
                data[new_key] = (test_files / data["file"]["file_name"]).open("rb")

            if method == "GET":
                if user_path["follow_redirects"]:
                    response = client.get(route, follow_redirects=True)
                else:
                    response = client.get(route)
            elif method == "POST":
                if user_path["follow_redirects"]:
                    response = client.post(
                        route,
                        data=data,
                        follow_redirects=True,
                        content_type="multipart/form-data",
                    )
                else:
                    response = client.post(route, data=data)

            else:
                raise ValueError("Invalid method")

        # assert the response status code
        assert response.status_code == user_path["assertions"]["status_code"]
        # if Location data then assert the Location of the response
        if "location" in user_path["assertions"]:
            if user_path["follow_redirects"]:
                assert response.request.path == user_path["assertions"]["location"]
            else:
                assert (
                    response.headers["Location"] == user_path["assertions"]["location"]
                )
        # assert the session data
        if "session" in user_path["assertions"]:
            for key, value in user_path["assertions"]["session"].items():
                assert session[key] == value
        # assert security keys in session data
        if "security_keys" in user_path["assertions"]:
            for key in user_path["assertions"]["security_keys"]:
                assert key in session["security_keys"]

        # assert content in the response
        if "content" in user_path["assertions"]:
            for content in user_path["assertions"]["content"]:
                assert content.encode("utf-8") in response.data
