# take in user choices, client and route_options and return a repsponse object


def user_actions(client, route_options: dict, user_choices: list):
    for choice in user_choices:
        # check if choice is in route_options, if not return error
        if choice not in route_options:
            raise ValueError(f"Choice not found in route_options: {choice}")
        route = route_options[choice]["route"]
        method = route_options[choice]["method"]
        data = route_options[choice]["data"]
        if method == "GET":
            response = client.get(route)
        elif method == "POST":
            response = client.post(route, data=data)

    return response
