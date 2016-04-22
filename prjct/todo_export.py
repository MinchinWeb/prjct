#!/usr/bin/env python
# -*- encoding: utf-8 -*-

'''
Export Todo and Done items.
'''

import json
import sys

import timestring

from topydo.cli.CLIApplicationBase import error
from topydo.lib import TodoFile
from topydo.lib.Sorter import Sorter
from topydo.lib.Config import config as topydo_config
from topydo.lib.Config import ConfigError
# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    topydo_config()
except ConfigError as config_error:
    error(str(config_error))
    sys.exit(1)

from topydo.lib.JsonPrinter import JsonPrinter
from topydo.lib import TodoList


def sorted_todos_by_project(cfg):
    ''' Takes our todo list, and returns two dictionaries of where the keys
        equal to the project name, and the value is a list of todo items under
        that project.

        - Note that a todo item may be appended to multiple second level HTML
            lists if the item is listed under multiple projects.
        - Note that todo items without a project are discarded.
        - Note that completed items beyond `completion_cutoff` (measured in
            days) are discarded.1
    '''
    '''
    print(type(cfg))
    print(cfg)
    print(type(cfg['todo']), cfg['todo'])
    print(type(cfg['todo']['completion_cutoff']), cfg['todo']['completion_cutoff'])
    '''
    completion_range = timestring.Range('last {!s} days'.format(cfg['todo']['completion_cutoff']))

    my_sorter = Sorter(p_sortstring=cfg['todo']['sort_string'])

    todofile = TodoFile.TodoFile(topydo_config().todotxt())
    # print('Loaded todo file from {}'.format(todofile.path))
    todotodos = TodoList.TodoList(todofile.read())
    # todolist = my_sorter.sort(todolist)            # in topydo v0.10
    # json_str = JsonPrinter().print_list(todolist)  # in topydo v0.10
    todolist = my_sorter.sort(todotodos.todos())
    todo_json_str = JsonPrinter().print_list(todolist)
    todo_json = json.loads(todo_json_str)

    donefile = TodoFile.TodoFile(topydo_config().archive())
    # print('Loaded done file from {}'.format(donefile.path))
    donetodos = TodoList.TodoList(donefile.read())
    donelist = my_sorter.sort(donetodos.todos())
    done_json_str = JsonPrinter().print_list(donelist)
    done_json = json.loads(done_json_str)

    active_todos = {}
    completed_todos = {}

    for my_json in [todo_json, done_json]:
        for todo in my_json:
            if not todo['completed']:
                for project in todo['projects']:
                    try:
                        active_todos[project].append(todo['source'])
                    except KeyError:
                        active_todos[project] = [todo['source']]
            else:
                completion_date = timestring.Date(todo['completion_date'])
                if completion_date in completion_range:
                    for project in todo['projects']:
                        try:
                            completed_todos[project].append(todo['source'])
                        except KeyError:
                            completed_todos[project] = [todo['source']]

    return active_todos, completed_todos


def to_html_dicts(cfg, indent='', open_icon='<i class="fa fa-square-o"></i> ',
                                  done_icon='<i class="fa fa-check-square-o"></i> '):
    ''' Takes our todo list, and returns two dictionaries of where the keys
        equal to the project name, and the value is a string of the todo items
        for that project as an HTML unordered list.

        - Note that a todo item may be appended to multiple second level HTML
            lists if the item is listed under multiple projects.
        - Note that todo items without a project are discarded.
        - Note that completed items beyond `completion_cutoff` (measured in
            days) are discarded.

        To make use of the default checkboxes, install FontAwesome in your page.

        Alternate icons:

        ```
        open_icon = '<input type="checkbox" disabled> '
        done_icon = '<input type="checkbox" disabled checked> '

        ```

        Args:
            indent  each line of the output is indented by this
    '''

    active_todos, completed_todos = sorted_todos_by_project(cfg)

    todo_html = {
        project.lower(): '{0}<ul class="prjct-task-list">\n\
                          {0}    <li class="prjct-task-list-item">{1}'.format(indent, open_icon) + \
                         '</li>\n{0}    <li class="prjct-task-list-item">{1}'.format(indent, open_icon).join(todo_list) + \
                         '</li>\n{0}</ul>'.format(indent)
        for project, todo_list in active_todos.items()
    }
    done_html = {
        project.lower(): '{0}<ul class="prjct-task-list">\n\
                          {0}    <li class="prjct-task-list-item">{1}'.format(indent, done_icon) + \
                         '</li>\n{0}    <li class="prjct-task-list-item">{1}'.format(indent, done_icon).join([todo[2:] for todo in todo_list]) + \
                         '</li>\n{0}</ul>'.format(indent)
        for project, todo_list in completed_todos.items()
    }

    return todo_html, done_html


def project_list():
    ''' Takes our todo list and our done list, and returns a (Python) list of
        all projects found.
    '''

    todofile = TodoFile.TodoFile(topydo_config().todotxt())
    # print('Loaded todo file from {}'.format(todofile.path))
    todotodos = TodoList.TodoList(todofile.read())
    todo_projects = todotodos.projects()

    donefile = TodoFile.TodoFile(topydo_config().archive())
    # print('Loaded done file from {}'.format(donefile.path))
    donetodos = TodoList.TodoList(donefile.read())
    done_projects = donetodos.projects()

    return list(todo_projects | done_projects)  # operater called 'join' and gives the union of the two sets

'''
if __name__ == '__main__':
    to_html_dicts()
'''
