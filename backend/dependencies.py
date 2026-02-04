from fastapi import Request

from services.analyzer import Analyzer


def get_analyzer(request: Request) -> Analyzer:
    """
    Get analyzer instance from app state.
    Used as a dependency in route handlers.
    """
    return request.app.state.analyzer


def get_settings(request: Request):
    """
    Get app settings from app state.
    """
    return request.app.state.settings
