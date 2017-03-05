"""Utility Functions."""

def sort_project_list(in_list):
    """
    Sort and clean up a list of projects.

    Removes duplicates and sorts alphabetically, case-insensitively.
    """
    # remove duplicate values if we ignore case
    # http://stackoverflow.com/a/27531275/4276230
    unique_projects_dict = {v.lower(): v for v in in_list}.values()
    unique_projects_list = list(unique_projects_dict)
    # sort the list, case insensitive
    sorted_project_list = sorted(unique_projects_list, key=str.lower)
    return sorted_project_list
