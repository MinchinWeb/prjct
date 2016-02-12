#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
prjct: Project Management for Living Life
"""

import json
import sys

import timestring

from topydo.cli.CLIApplicationBase import error
from topydo.lib import TodoFile
from topydo.lib.Config import config, ConfigError
# First thing is to poke the configuration and check whether it's sane
# The modules below may already read in configuration upon import, so
# make sure to bail out if the configuration is invalid.
try:
    config()
except ConfigError as config_error:
    error(str(config_error))
    sys.exit(1)

from topydo.lib.JsonPrinter import JsonPrinter
from topydo.lib import TodoList


def to_html_dicts(completion_cutoff=30):
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

    todofile = TodoFile.TodoFile(config().todotxt())
    # print('Loaded todo file from {}'.format(todofile.path))
    todolist = TodoList.TodoList(todofile.read())
    # json_str = JsonPrinter().print_list(todolist)  # in topydo v0.10
    todo_json_str = JsonPrinter().print_list(todolist.todos())
    todo_json = json.loads(todo_json_str)

    donefile = TodoFile.TodoFile(config().archive())
    # print('Loaded done file from {}'.format(donefile.path))
    donelist = TodoList.TodoList(donefile.read())
    done_json_str = JsonPrinter().print_list(donelist.todos())
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
        project.lower(): '<ul class="task-list"><li class="task-list-item"><input type="checkbox" disabled>' + \
                         '</li><li class="task-list-item"><input type="checkbox" disabled>'.join(todo_list) + \
                         '</li></ul>'
        for project, todo_list in active_todos.items()
    }
    done_html = {
        project.lower(): '<ul class="task-list"><li class="task-list-item"><input type="checkbox" disabled checked>' + \
                         '</li><li class="task-list-item"><input type="checkbox" disabled checked>'.join([todo[2:] for todo in todo_list]) + \
                         '</li></ul>'
        for project, todo_list in completed_todos.items()
    }

    return todo_html, done_html

if __name__ == "__main__":
    to_html_lists()
