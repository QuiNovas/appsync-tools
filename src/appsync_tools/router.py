#!/usr/bin/env python3.8
from typing import Any, Callable, Union
from typeguard import typechecked
from .exceptions import NonExistentRouteException


class Router:
    def __init__(self):
        self.routes = {}

    @typechecked
    def default_route(self, func: Callable[[dict], Any]) -> Callable[[dict], Any]:
        """
        Sets the default route
        Return value:
        returns a function that must accept a dict as its sole argument
        """
        self.routes["default"] = func
        return func

    @typechecked
    def route(self, route: Union[str, list]) -> Callable[[dict], Any]:
        """
        Accept a route and return a decorated function after passing that function
        to the dict of routes to be called by handle_route

        Keyword arguments:
        route: An appsync route expressed as <parent type>.<object type>

        Return value:
        returns a function that must accept a dict as its sole argument
        """

        @typechecked
        def inner(func: Callable[[dict], Any]) -> Callable[[dict], Any]:
            """
            Accepts a function that accepts a dict as its sole argument, adds the
            function to the current class object's map of routes to functions,
            and returns the function
            """
            if isinstance(route, list):
                for r in route:
                    self.routes[r] = func
            else:
                self.routes[route] = func

            return func
        return inner

    @typechecked
    def handle_route(self, event: dict) -> Any:
        """
        Looks up the route for a call based on the parentType and field in event["info"]
        The event arg must, at minimum, contain the info dict that Appsync places inside of the Lambda event.
        The event arg is the sole argument passed to the route handler. If the route doesn't exist and
        default_route is None, then appsync_tools.exceptions.NonExistentRoute will be raised
        """
        field = event["info"]["parentType"]
        subfield = event["info"]["field"]
        route = f"{field}.{subfield}"
        if route in self.routes:
            handler = self.routes[route]
        elif self.routes.get("default") is not None:
            handler = self.routes["default"]
        else:
            raise NonExistentRouteException(f"Route {route} does not exist")

        handler(event)
