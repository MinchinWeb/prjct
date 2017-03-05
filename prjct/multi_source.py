#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""These are elements relating to data merged from multiple sources."""


from . import config as prjct_config
from . import todo_export
from . import descriptions
from . import __version__


def project_list():
    """
    Create a full list of projects.

    Merges the projects lists from the todo file, the done file, and the
    description files.
    """
    cfg = prjct_config.load()

    todo_done_projects = set(todo_export.project_list())
    desc_projects = set(descriptions.project_list(cfg))

    # operator called 'join' and gives the union of the two sets
    all_projects_list = list(todo_done_projects | desc_projects)
    # remove duplicate values if we ignore case
    # http://stackoverflow.com/a/27531275/4276230
    unique_projects_dict = {v.lower(): v for v in all_projects_list}.values()
    unique_projects_list = list(unique_projects_dict)
    # sort the list, case insensitive
    sorted_project_list = sorted(unique_projects_list, key=str.lower)
    return sorted_project_list


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
