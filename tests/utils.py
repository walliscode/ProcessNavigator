from pathlib import Path


"""Utility functions for tests."""


# takes in multiple paths and stacks the response for each path
# this allows for session keys to be used organically
def provide_stacked_response(client, paths, route_options):
    response = client.get("/")
    for path in paths:
        print("stacking path: ", path)
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
            print("GET: ", route)
            if "follow_redirects" in route_info:
                response = client.get(route, follow_redirects=True)
            else:
                response = client.get(route)
        elif method == "POST":
            print("POST: ", route)
            if "follow_redirects" in route_info:
                response = client.post(route, data=data, follow_redirects=True)
            else:
                response = client.post(route, data=data)

        else:
            raise ValueError("Invalid method")

    return response
