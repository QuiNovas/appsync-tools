#!/usr/bin/env python3.8
from .exceptions import NonExistentRouteException


class Router:
    def __init__(self):
        self.routes = {}

    def route(self, route):
        def return_func(func):
            if isinstance(route, list):
                for r in route:
                    self.routes[r] = func
            else:
                self.routes[route] = func
            return func
        return return_func

    def handle_route(self, event):
        field = event["info"]["parentType"]
        subfield = event["info"]["field"]
        current_route = f"{field}.{subfield}"
        try:
            current_handler = self.routes[current_route]
            current_handler(event)
            is_error = False
        except (NameError, KeyError):
            is_error = True

        if is_error:
            raise NonExistentRouteException(f"Route {current_route} does not exist")
