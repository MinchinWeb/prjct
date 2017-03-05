#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
Tests the `todo_export.to_html_dicts() function by generate a webpage
containing their results.
"""
from datetime import datetime
import os
from pathlib import Path
import unittest

import prjct
from prjct.todo_export import to_html_dicts


class TestTodoExport(unittest.TestCase):

    # TODO: Add setup that removes all files in test/results directory

    def test_to_html_lists(self):
        p = Path(__file__)  # location of this file
        OUTPUT_FILE_NAME = 'test_todo_export.html'
        output_file = p.parent / 'results' / OUTPUT_FILE_NAME

        todos, dones = to_html_dicts(prjct.config.load())

        todos_split = "\n".join(["<h3>" + project + "</h3>" + todo_list for project, todo_list in todos.items()])
        dones_split = "\n".join(["<h3>" + project + "</h3>" + done_list for project, done_list in dones.items()])

        html = """\
        <html>
            <head>
                <title>prjct -- todo_export.to_html_dicts() function test</title>
            </head>
            <body>
                <h1>prjct -- todo_export.toto_html_dicts() function test</h1>
                <p>{}</p>
                <h2>My To-do Items</h2>
                {}
                <h2>My Done Items</h2>
                {}
                <hr />
                <p>prjct v.{} -- test run {}</p>
            </body>
        </head>
        """.format(prjct.__doc__, todos_split, dones_split, prjct.__version__, datetime.now())

        output_file.write_text(html)

        self.assertTrue(os.path.isfile(str(output_file)))


if __name__ == '__main__':
    unittest.main()
