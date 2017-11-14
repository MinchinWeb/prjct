prjct
=====

Project Management for Living Life, v0.6, 2017-11-13

.. note:: Not all features have been implemented yet. I use this day-to-day, but really, it's alpha-level software.

Background
----------

I have used todo lists to manage my workload for many years. I have also found
several good programs for managing my todo list, particularly when using a flat
text file (*a la* todo.txt) Recently, after hearing many good things about
*Getting Things Done*, I picked up the book. As I understand it, he recommends
that your todo list actually become more of a 'next items' list, derived from
your project list. I couldn't find anything particularly suited to this, so I
decided to write something myself.

Goal
----

Manage my project list, and from this derive my todo list.

Philosophy
----------

A couple of philosophical notes that are built in to this project:

* where possible, data should be stored in text files. Furthermore, these text
   files should be editable on the go with a simple text editor.
* a 'project' is some end goal that requires more than one action
* by writing everything that needs done down, I can spend my mental energy on
   projects other than remembering what needs to be done. This only works if it
   is easy, at a glance, to review what I need to do next.
* if something exists that does the job well, there is no need to rebuild it

Programming Language
--------------------

Python 3.5 on Windows.

jrnl Integration
''''''''''''''''

``jrnl`` is a command line program written in Python. It allows notes to be
written in plain text, and has various importers and exporters. The thought is
to write a note in ``jrnl`` about a project, and include todo items as part of
the note. The though was to use the checkbox style used on GitHub.

So an entry might look like:

.. code-block:: text

    [2015-07-20 20:34] Project Update -- July 20

    All about my new project...blah, blah, blah.

    More about my project.

    - [ ] something that needs done
    - [ ] some other todo item

    +Project_Name


Todo items in an entry would automatically be assigned the creation date of
the entry, and any tags on the entry would apply to the todo items in that
entry.

Pelican Integration
'''''''''''''''''''

*Pelican* integration has been deprciated in favour of Sphinx, which now
allows *jrnl* content to be written in Markdown, but allows more powerful
control of the rest of the site presentation.

Sphinx Integration
''''''''''''''''''

*Sphinx* is a static site generator, originally concieved for generating
Python documentation, written in Python. Currently, entries from
*jrnl* can be exported to Markdown formatted text files, and these text files
can then be fed to *Sphinx* to create a blog using the *ABlog* extension.
*prjct* can build on this behaviour. For each defined project, a page,
similar to a tag page, will be generated. This page will list the project
overview, a list of the open todo items, the recently completed items, and then
a list entries tagged with the project name.

todo.txt Integration
''''''''''''''''''''

One of the goals of *prjct* is to allow other todo.txt clients to manage the
todo list. To this end, a *todo.txt* and a *done.txt* file will need to be
maintained. As well, items that are added directly to the todo list (rather
that through a *jrnl* entry) will be directly added to the *todo.txt* file.

When run, *prjct* would add new items in *jrnl* entries to the *todo.txt*
file, and update completed tasks from the *done.txt* file listed in *jrnl*
entries.

To cross-reference todo items in *jrnl* entries and on *todo.txt*, I propose
adding a 'key' to each item. I haven't decided what format to use for the key.
One option is using a UUID (128 bits, base 16, typically 35 characters).
Another option is to use
`base32 crockford <https://pypi.python.org/pypi/base32-crockford/0.3.0>`_ which
could be variable length, but packs 5 bits per character instead of 4,
decreasing key lengths by 25% for keys in the same sample space.

The advantage of using UUID's is they look like numbers because they have so
many digits in them. In either case, we may be by referring to items by a
shortened version of the identifier, a little like *git* treats commit ID's.

So a todo item might look like this:

.. code-block:: text

    2015-07-20 Some item that needs doing +my_project due:2016-01-01 t:2015-12-01 prjct:d95ff071-9443-49f0-8f11-b2787649a481

(*due* refers to when the task is due; *t* refers to the "threshold date",
i.e. don't show this task before this date; *prjct* is our added key (in this
case, an UUID)).

prjct.txt
'''''''''

This is a file listing all projects. Format somewhat based on *todo.txt*. One
project per line. Projects with the context *@someday* will not be considered
when the user reviews project, unless he explicitly asks to review them.

Packaged Format
---------------

In three stages:

1. Python script installable via *pip*
2. self-contained Windows exe (still command line)
3. self-contained Windows exe with GUI (although that GUI was effectively be a website)

Libraries / Supporting Programs
-------------------------------

* Python
* `jrnl <https://github.com/maebert/jrnl>`_ -- useful to store general notes
* `topydo <https://github.com/bram85/topydo>`_ -- todo list manager
* `click <http://click.pocoo.org/6/>`_ -- for managing command line options
* *todo.txt*
* `Sphinx <http://www.sphinx-doc.org/>`_ -- static site generator
* `ABlog <https://ablog.readthedocs.org/>`_ -- blogging extention to Sphinx
* `Travis-CI <https://travis-ci.org/>`_ -- for automated testing

Data File Structure
-------------------

.. code-block:: text

    .prjct\
      |- .prjct-config                  (configuration file)
      |- jrnl.txt                       (jrnl entries)
      |- todo.txt                       (todo items)
      |- done.txt                       (completed todo items)
      |- prjct.txt                      (list of all projects)
      |- source\                        (used as the Sphinx source files)
      |    |- _static                   (folder for storage of images, etc)
      |    |- docs                      (folder contain documenation for
      |    |                              getting prjct, including
      |    |                              philosopy, started, etc.)
      |    |- jrnl                      (temporary folder holding Markdown
      |    |    |                         export of jrnl entries)
      |    |    |- 2015-07-20_project_entry.md
      |    |    ` ...
      |    |- prjct                     (temporary folder holding reST
      |    |    |                         export of project overviews)
      |    |    |- my_project_name.rst
      |    |    ` ...
      |    |- conf.py                   (Sphinx main configuraiton file)
      |    `- index.rst                 (source page for website front
      |                                   page)
      `- build
           `- dirhtml                   (Exported Sphinx site)
                |- index.html
                ` ...

Usage
-----

.. code-block:: text

    Project Management

    Usage:
      prjct [options]
      prjct.py [options]
      prjct usage           Displays this screen and exits
      prjct review          Review all projects listed in in the prjct.txt
                                file to ensure they all have a next item.
                                If there is nonext item, you are asked to
                                either select one ofthe existing todo
                                items, or add a new one
      prjct (ls | list)     List all projects in the default prjct.txt
                                file
      prjct add <project>   Add a project to the list
      prjct rm <project number>
                            Remove a project from the list
      prjct someday <project number>
                            Move a project from the default list to the
                                someday list
      prjct goal (project number | project name)
                            Displays the goal for a given project
      prjct generate        Generates a list of project based on your todo
                                list
      todo top              List top todo items
      todo add <item>       Add an item to the todo list
      todo do <item>...     Do item on todo.txt
      todo pri <item>... <priority>
                            Changes (or adds) the priority (A-Z) to the
                                given todo item(s)
      todo depri <item>... <priority>
                            Removes the priority to the given todo item(s)
      todo (ls | list) [filter text]
                            Lists all items on the todo list after
                                applying the filter
      jrnl [jrnl options]   calls the jrnl program; allows entry of goals,
                                notes, etc
      prjct report          Generates a report listing all projects,
                                goals, notes, done todo items, and
                                outstanding todo items
      todo context          Generates a report, listed all todo items,
                                which each context in a separate file
      prjct about           Displays a more complete 'version' page,
                                including the goals of the project and
                                import dates
      prjct changes         Displays the changelog
      prjct credits         Displays all contributors to the project
      prjct (phil | philosophy)
                            Displays some philosophical thoughts on how to
                                get the most out of the system
      prjct howto           Displays a basic tutorial on how to use the
                                program

    Options:
      -h --help                         Dispalys a list of available
                                            commands, recommends running
                                            'usage' for more details, and
                                            exits
      -v --version                      Show version, and exit
      --config=<path to .prjct-config>  Select a configuration file
      --todo=<path to todo.txt file>    Select a todo.txt file
      --done=<path to done.txt file>    Select a done.txt file (completed
                                            todo items)
      --prjct=<path to prjct.txt file>  Select a prjct.txt file (project
                                            list)
      --export=<path>                   Specify the export path

Goals are pulled *jrnl* by filtering for entries tagged with the project name
and looking for a *Goal* heading.

Getting Things Done -- 7 lists
------------------------------

In *Getting Things Done*, he mentions 7 types lists to manage:

* a projects list
* project support material
* calendared actions and information
* a waiting for list
* reference material
* a someday/maybe list

This project aims mainly to maintain the first -- the project list. Some project
support material can to provided using ``jrnl`` (particularly goals), but most
will be kept elsewhere. Nothing is a attempted (yet) with either calendared
items or the 'tickler' file he mentions in the book. A 'waiting for' list can
quasi implemented by assigning the tasks in question a (W) priority. Reference
material is intended to be kept elsewhere. The 'someday/maybe' project list
is designed, ultimately, to be supported.

.. for Version History, see CHANGELOG.rst

.. toctree::
   :hidden:

   prjct Changelog
   *
