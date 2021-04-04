"""Functions that can be used ANYWHERE!"""
import os


def get_project_root() -> str:
    """Returns an absolute path to this project"""
    current_directory = os.path.dirname(__file__)
    app_directory = os.path.dirname(current_directory)
    project_root = os.path.dirname(app_directory)

    return project_root
