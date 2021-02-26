#!/usr/bin/env python3.8
from typing import Any, Callable, Union
from .exceptions import NonExistentRouteException


class Router:
    def __init__(self):
        self.routes = {}
        self._default_route = None

    @property
    def default_route(self) -> Union[Callable[[dict], Any], None]:
        return self._default_root

    @default_route.setter
    def default_route(self, func: Callable[[dict], Any]) -> Callable[[dict], Any]:
        """
        When set will match any route passed to handle_route that has no function
        attached
        """
        self._default_route = func

    def route(self, route: Union[str, list]) -> Callable[[dict], Any]:
        """
        Accept a route and return a decorated function after passing that function
        to the dict of routes to be called by handle_route

        Keyword arguments:
        route: An appsync route expressed as <parent type>.<object type>

        Return value:
        returns a function that must accept a dict as its sole argument
        """
        def return_func(func: Callable[[dict], Any]) -> Callable[[dict], Any]:
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
        return return_func

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
        elif self._default_route is not None:
            handler = self._default_route
        else:
            raise NonExistentRouteException(f"Route {route} does not exist")

        handler(event)
