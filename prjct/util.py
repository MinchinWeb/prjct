"""Utility Functions."""

def sort_project_list(in_list):
    """
    Sort and clean up a list of projects.

    Removes duplicates and sorts alphabetically, case-insensitively.
    """
    # replace spaces with underscores
    in_list_2 = [i.replace(" ", "_") for i in in_list]
    # remove duplicate values if we ignore case
    # http://stackoverflow.com/a/27531275/4276230
    unique_projects_dict = {v.lower(): v for v in in_list_2}.values()
    unique_projects_list = list(unique_projects_dict)
    # lowercase
    lowercase_list = [i.lower() for i in unique_projects_list]
    # sort the list
    sorted_project_list = sorted(lowercase_list)
    return sorted_project_list
