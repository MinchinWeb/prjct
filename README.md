# prjct

Project Management

*Version*: 0.1, 2013-11-30

## Background

I have used todo lists to manage my workload for many years. I have also found
several good programs for managing my todo list, particularly when using a flat
text file (*a la* todo.txt) Recently, after hearing many good things about
*Getting Things Done*, I picked up the book. As I understand it, he recommends
that your todo list actually become more of a 'next items' list, derived from
your project list. I couldn't find anything particularly suited to this, so I
decided to write something myself.

## Goal

Manage my project list, and from this derive my todo list.

## Philosophy

A couple of philosophical notes that are built in to this project:

* where possible, data should be stored in text files. Further more, these text
files should be editable on the go with a simple text editor.
* a 'project' is some end goal that requires more than one action
* by writing everything that needs done down, I can spend my mental energy on
projects other than remembering what needs to be done. This only works if it is
easy, at a glance, to review what I need to do next.
* if something exists that does the job well, there is no need to rebuild it

## Programming Language

Python 2.7 on Windows

## Packaged Format

In three stages:

1. self-installable Python scripts
2. Python script installable vai `pip`
3. self contained Windows exe (still commandline)

## Libraries / Supporting Programs

* Python
* [jrnl](https://github.com/maebert/jrnl)
* todo manager - I haven't found a good Python todo manager quite yet. I'll keep
looking
* [docopt](http://docopt.org/) - for managing command line options
* Travis-CI - for automated testing

## Data File Structure

```
.prjct\
  |- .prjct-config					(configuration file)
  |- prjct.txt						(main project list)
  |- someday.txt					(alternate project list)
  |- ....txt
  |- todo.txt						(todo items)
  |- done.txt						(completed todo items)
  +- reports\
       |- prjct-report.txt			(full report)
	   |- prjct-report.md			(full report, exported in Markdown)
	   |- @errands-todo.txt			(todo items by context)
	   |- @...-todo.txt
	   |- +my_project-report.txt	(report by project)
	   +- +...-report.txt
```
<!-- _ -->

## Usage
```python
"""Project Management

Usage:
  prjct [options]
  prjct.py [options]
  prjct usage			Displays this screen and exits
  prjct review			Review all projects listed in in the prjct.txt file to
							ensure they all have a next item. If there is no
							next item, you are asked to either select one of
							the existing todo items, or add a new one
  prjct (ls | list)		List all projects in the default prjct.txt file
  prjct add <project>	Add a project to the list
  prjct rm <project>	Remove a project from the list
  prjct someday <project number>
						Move a project from the default list to the someday
							list
  prjct goal (project number | project name)
						Displays the goal for a given project
  prjct top				List top todo items
  prjct do <item>...	Do item on todo.txt
  prjct pri <item>... <priority>
						Changes (or adds) the priority (A-Z) to the given todo
							item(s)
  prjct depri <item>... <priority>
						Removes the priority to the given todo item(s)
  prjct jrnl [jrnl options]
						calls the jrnl program; allows entry of goals, etc
  prjct report [project]
						Generates a report listing all projects, goals, done
							todo items, and outstanding todo items
  prjct todo [filter text]
						Lists all items on the todo list after applying the
							filter
  prjct context			Generates a report, listed all todo items, which each
							context in a separate file
  prjct about			Displays a more complete 'version' page, including
							the goals of the project and import dates
  prjct changes			Displays the changelog
  prjct credits			Displays all contributors to the project
  prjct (phil | philosophy)
						Displays some philosophical thoughts on how to get the
							most out of the system
  prjct howto			Displays a basic tutorial on how to use the program

Options:
  -h --help							Dispalys a list of available commands,
										recommends running 'usage' for more
										details, and exits
  -v --version						Show version, and exit
  --config=<path to .prjct-config>	Select a configuration file
  --todo=<path to todo.txt file>	Select a todo.txt file
  --done=<path to done.txt file>	Select a done.txt file (completed todo
									items)
  --prjct=<path to prjct.txt file>	Select a prjct.txt file (project list)
  --export=<file>					Specify the export path
  --markdown						Export in Markdown formatted text
"""
```

Goals are pulled `jrnl` by filtering for entries tagged with the project name
and '@goal'.
