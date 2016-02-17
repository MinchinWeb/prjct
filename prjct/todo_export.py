#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Export Todo and Done items.
"""

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

from .config import COMPLETION_CUTOFF, TODO_SORT_STRING


def to_html_dicts(completion_cutoff=COMPLETION_CUTOFF):
    ''' Takes our todo list, and returns two dictionaries of where the keys
        equal to the project name, and the value is a string of the todo items
        for that project as an HTML unordered list.

        - Note that a todo item may be appended to multiple second level HTML
            lists if the item is listed under multiple projects.
        - Note that todo items without a project are discarded.
        - Note that completed items beyond `completion_cutoff` (measured in
            days) are discarded.
    '''

    completion_range = timestring.Range('last {} days'.format(completion_cutoff))

    my_sorter = Sorter(p_sortstring=TODO_SORT_STRING)

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

    todo_html = {
        project.lower(): '<ul class="prjct-task-list"><li class="prjct-task-list-item"><input type="checkbox" disabled>' + \
                         '</li><li class="prjct-task-list-item"><input type="checkbox" disabled>'.join(todo_list) + \
                         '</li></ul>'
        for project, todo_list in active_todos.items()
    }
    done_html = {
        project.lower(): '<ul class="prjct-task-list"><li class="prjct-task-list-item"><input type="checkbox" disabled checked>' + \
                         '</li><li class="prjct-task-list-item"><input type="checkbox" disabled checked>'.join([todo[2:] for todo in todo_list]) + \
                         '</li></ul>'
        for project, todo_list in completed_todos.items()
    }

    return todo_html, done_html

if __name__ == "__main__":
    to_html_dicts()
