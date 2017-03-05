#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""These are elements relating to data merged from multiple sources."""


from . import config as prjct_config
from . import __version__, descriptions, todo_export
from .util import sort_project_list


def project_list():
    """
    Create a full list of projects.

    Merges the projects lists from the todo file, the done file, the
    description files, and the project configuration.
    """
    cfg = prjct_config.load()

    todo_done_projects = set(todo_export.project_list())
    desc_projects = set(descriptions.project_list(cfg))
    config_projects = set(prjct_config.project_list())

    # operator called 'join' and gives the union of the two sets
    all_projects_list = list(todo_done_projects | desc_projects |
                             config_projects)
    return sort_project_list(all_projects_list)


def active_project_list():
    """
    Create a full list of projects.

    Merges the projects lists from the todo file, the done file, the
    description files, and the project configuration.
    """
    all_projects = project_list()

    completed_projects = set(prjct_config.compeleted_projects())
    someday_projects = set(prjct_config.someday_projects())

    exclude_projects = list(completed_projects | someday_projects)
    exclude_projects_2 = sort_project_list(exclude_projects)

    my_project_list = [i for i in all_projects if i not in exclude_projects_2]

    return sort_project_list(my_project_list)



def all_projects_entry():
    """Create a (basic) markdown entry that is tagged with all projects."""
    all_tags_str = ', '.join(project_list())
    cfg = prjct_config.load()

    my_entry = """\
title: All Projects
date: {}
tags: {}

This is a placeholder entry created by *prjct* v.{}, tagged with all projects
listed on your todo list, your done lists, and your project description files.
""".format(cfg['export']['all_projects_date'], all_tags_str, __version__)

    return my_entry
