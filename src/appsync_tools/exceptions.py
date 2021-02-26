#!/usr/bin/env python3.8


class AppsyncRouterException(Exception):
    pass


class NonExistentRouteException(AppsyncRouterException):
    def __init__(self, *args, **kwargs):
        default_message = "Route does not exist"
        if not (args or kwargs): args = (default_message,)
        super().__init__(*args, **kwargs)
