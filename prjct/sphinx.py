#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Generate Sphinx source files
'''

from pathlib import Path

import winshell
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

    # everything but documentation front page
    docs_files = []

    if relative_path:
        export_loc = Path.cwd() / export_path / '.no-file'
    else:
        # we have an absolute path
        export_loc = Path(export_path)

    # make the folder if it doesn't exist
    export_loc.parent.mkdir(exist_ok=True)

    # copy over readme as front page of documentation
    # TODO: readme to have toctree containing the rest of the documentation
    dest_loc = export_loc.with_name('index.rst')
    try:
        winshell.delete_file(str(dest_loc), no_confirm=True)
    except winshell.x_winshell:
        pass
    winshell.copy_file(str(readme_loc), str(dest_loc), rename_on_collision=False)

    # copy over everything else
    for my_file in docs_files:
        # with Python 3.5.2 use `readme_loc.path`
        dest_loc = export_loc.with_name(my_file.name)
        try:
            winshell.delete_file(str(dest_loc), no_confirm=True)
        except winshell.x_winshell:
            pass
        winshell.copy_file(str(my_file), str(dest_loc), rename_on_collision=False)


def generate_project_summaries(export_path=SPHINX_PROJECT_SOURCES, relative_path=True):
    ''' Generates prjct's summeries of the user's projects. '''

    if relative_path:
        export_loc = Path.cwd() / export_path / '.no-file'
    else:
        # we have an absolute path
        export_loc = Path(export_path)

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
    todo_project_list_lower = []
    for project in todo_project_list:
        project_list.append(project.lower())
        todo_project_list_lower.append(project.lower())

    project_list = set(project_list)

    todo_html, done_html = todo_export.to_html_dicts(indent=" "*4)

    # for project_name in project_list:
    # only do projects with todo and done items (or project summaries, when we get those defined)
    for project_name in todo_project_list_lower:
        html_parts = ['']*6

        html_parts[0] = '{} Summary'.format(project_name)
        html_parts[1] = '='*len(html_parts[0]) + '\n'
        html_parts[2] = ''  # project summary
        if todo_html.get(project_name):
            html_parts[3] = 'To-Do Items\n-----------\n\n.. raw :: html\n\n{}\n'.format(todo_html.get(project_name))
        if done_html.get(project_name):
            html_parts[4] = 'Done Items\n----------\n\n.. raw :: html\n\n{}\n'.format(done_html.get(project_name))
        if project_name in jrnl_projects:
            html_parts[5] = 'Notes\n-----\n\n.. postlist::\n   :tags: {}\n   :date: %A, %B %d, %Y\n   :list-style: circle\n   :format: {{title}} on {{date}}\n   :excerpts:\n'.format(project_name)

        my_html = '\n'.join(html_parts)

        dest_loc = export_loc.with_name('{}.rst'.format(project_name))
        dest_loc.write_text(my_html)


def geneate_projects_page(export_path=(SPHINX_PROJECT_SOURCES + '/index.rst'), relative_path=True):
    ''' Generates the 'front page' for our projects. Lists each project with
        its next todo item.
    '''

    if relative_path:
        export_loc = Path.cwd() / export_path
    else:
        # we have an absolute path
        export_loc = Path(export_path)

    todo_project_list = todo_export.project_list()
    # add projects with defined scopes to this list

    # sort alphabetically, case-insensitive, by project
    project_list = sorted(todo_project_list, key=lambda i: str(i[0]).lower())

    active_todos, _ = todo_export.sorted_todos_by_project()

    # create a list of tuples of each project and it's top rated item
    table_prep = []
    for project in project_list:
        table_prep.append((project, active_todos.get(project, ['*None*'])[0]))

    # get the longest project title
    table_width_1 = len(sorted(table_prep, key=lambda i: len(i[0]))[-1][0])
    # get the longest project item
    table_width_2 = len(sorted(table_prep, key=lambda i: len(i[1]))[-1][1])
    #print(table_width_1, table_width_2)

    my_html = 'All Projects\n============\n\n'
    my_html += '='*(table_width_1*2 + 10) + ' ' + '='*table_width_2 + '\n'
    for project in table_prep:
        my_html += ':doc:`{0} <{2}>`{width} {1}\n'.format(project[0].replace('_', ' '), project[1], project[0].lower(), width=' '*2*(table_width_1-len(project[0])))
    my_html += '='*(table_width_1*2 + 10) + ' ' + '='*table_width_2 + '\n'

    my_html += '\n\n.. :toctree::\n    :hidden:\n    :glob:\n\n    *\n'

    export_loc.write_text(my_html)
