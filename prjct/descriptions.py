#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
For dealing with project descriptions.

Descriptions are assumed to be provided as a collection of markdown files,
named '{project_name}.md'
"""

from pathlib import Path

from markdown import markdown

from . import config as prjct_config
from . import __version__
from .config import MARKDOWN_EXT
from .exceptions import ConfigKeyMissingError


def file_path(cfg):
    """
    Return the directory containing the description files as an absolute path.

    Returns None if the configuration does not define this.
    """
    try:
        desc_path = Path(cfg['descriptions_dir'])
    except KeyError:
        raise ConfigKeyMissingError('description_dir')

    # if the path is relative, convert to an absolute path
    if not desc_path.is_absolute():
        desc_path = Path(prjct_config.CONFIG_FILE_PATH).parent / desc_path

    # make the folder, if it doesn't exist yet
    desc_path.mkdir(exist_ok=True)

    return str(desc_path)


def project_list():
    """
    Return a list of the projects for which the appropriate description file can be found.

    Returns an empty list is the description filepath is not defined in the
    configuration.
    """
    cfg = prjct_config.load_or_install_prjct()
    # descriptions folder
    try:
        desc_path = Path(file_path(cfg))
    except ConfigKeyMissingError:
        return []

    projects = []

    for my_file in desc_path.iterdir():
        if my_file.suffix in MARKDOWN_EXT:
            projects.append((my_file.stem).lower())

    return projects


def to_markdown_dicts():
    """
    Takes our project description folder, and returns a dictionary where the
    keys equal to the project name, and the value is the contents of project
    description file as unprocessed, raw text.
    """
    cfg = prjct_config.load_or_install_prjct()

    try:
        desc_path = Path(prjct_config.CONFIG_FILE_PATH).parent / cfg['descriptions_dir']
    except ConfigKeyMissingError:
        return {}

    markdown_dict = {}

    for my_file in desc_path.iterdir():
        if my_file.suffix in MARKDOWN_EXT:
            markdown_dict[(my_file.stem).lower()] = my_file.read_text()

    return markdown_dict


def to_html_dict(*, markdown_extension_config=None):
    """
    Takes our project description folder, and returns a dictionary where the
    keys equal to the project name, and the value is the contents of project
    description file as processed markdown (i.e. raw HTML).

    Args:
        markdown_extentions     A list of markdown extensions, passed
                                transparently through to the markdown
                                render.
    """
    if markdown_extension_config is None:
        markdown_extension_config = {}
    markdown_dict = to_markdown_dicts()
    extensions = [k for k, _ in markdown_extension_config.items()]
    html_dict = {}

    for k, v in markdown_dict.items():
        html_dict[k] = markdown(v, extensions=extensions,
                                extension_config=markdown_extension_config)

    return html_dict


def all_projects_entry():
    """Create a (basic) markdown entry that is tagged with all projects."""
    cfg = prjct_config.load()
    all_tags_str = ', '.join(project_list(cfg))

    my_entry = """\
title: All Projects
date: {}
tags: {}

This is a placeholder entry created by *prjct* v.{}, tagged with all projects
with description files.
""".format(cfg['export']['all_projects_date'], all_tags_str, __version__)

    return my_entry
