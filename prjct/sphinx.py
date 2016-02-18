#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Generate Sphinx source files
'''

from pathlib import Path

import winshell
#import jrnl
import jrnl.install as jrnl_install
import jrnl.util as jrnl_util
import jrnl.Journal as jrnl_Journal
import jrnl.plugins.util as jrnl_plugins_util

from .config import SPHINX_DOC_SOURCES, SPHINX_PROJECT_SOURCES, JOURNALS
from . import todo_export


def generate_prjct_docs(export_path=SPHINX_DOC_SOURCES, relative_path=True):
    ''' Generates prjct's included documentation sources, and exports it to the
        `export_path`.
    '''

    here = Path(__file__)
    readme_loc = here.parent / '..' / 'README.rst'

    docs_files = [readme_loc]

    if relative_path:
        export_loc = Path.cwd() / export_path / '.no-file'
    else:
        # we have an absolute path
        export_loc = export_path

    # make the folder if it doesn't exist
    export_loc.parent.mkdir(exist_ok=True)

    for my_file in docs_files:
        # with Python 3.5.2 use `readme_loc.path`
        dest_loc = export_loc.with_name(my_file.name)
        winshell.delete_file(str(dest_loc), no_confirm=True)
        winshell.copy_file(str(my_file), str(dest_loc), rename_on_collision=False)


def generate_project_summaries(export_path=SPHINX_PROJECT_SOURCES, relative_path=True):
    ''' Generates prjct's summeries of the user's projects. '''

    if relative_path:
        export_loc = Path.cwd() / export_path / '.no-file'
    else:
        # we have an absolute path
        export_loc = export_path

    # make the folder if it doesn't exist
    export_loc.parent.mkdir(exist_ok=True)

    project_list = []
    # get list of projects from Jrnl
    all_journal_config = jrnl_install.load_or_install_jrnl()
    for journal_name in JOURNALS:
        journal_config = jrnl_util.scope_config(all_journal_config, journal_name)
        journal = jrnl_Journal.open_journal(journal_name, journal_config)
        jrnl_project_list = jrnl_plugins_util.get_tags_count(journal)

        for _, project in jrnl_project_list:
            project_list.append(project[1:].lower())  # remove tag symbol from front
    jrnl_projects = list(project_list)  # make a copy

    # get list of projects with defined scopes...

    # get a list of projects from our todo and done lists
    todo_project_list = todo_export.project_list()
    for project in todo_project_list:
        project_list.append(project.lower())

    project_list = set(project_list)

    todo_html, done_html = todo_export.to_html_dicts(indent=" "*4)

    for project_name in project_list:
        html_parts = ['']*6

        html_parts[0] = '{} Summary'.format(project_name)
        html_parts[1] = '='*len(html_parts[0]) + '\n'
        html_parts[2] = ''  # project summary
        if todo_html.get(project_name.lower()):
            html_parts[3] = 'To-Do Items\n-----------\n\n.. raw :: html\n\n{}\n'.format(todo_html.get(project_name))
        if done_html.get(project_name.lower()):
            html_parts[4] = 'Done Items\n----------\n\n.. raw :: html\n\n{}\n'.format(done_html.get(project_name))
        if project_name in jrnl_projects:
            html_parts[5] = 'Notes\n-----\n\n.. postlist::\n   :tags: {}\n   :list-style: circle\n   :format: {{title}} on {{date}}\n   :excerpts:\n   :sort:\n'.format(project_name)

        my_html = '\n'.join(html_parts)

        dest_loc = export_loc.with_name('{}.rst'.format(project_name))
        dest_loc.write_text(my_html)
