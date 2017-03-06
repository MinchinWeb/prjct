"""Test list generation functionality."""

import unittest
from pathlib import Path

import prjct


class TestListGeneration(unittest.TestCase):
    """Generate Lists."""

    here = Path(__file__).parent
    config_file = here / "data" / "list_filtering.yaml"
    # paths (in following file) are relative from the project root
    todo_config_file = here / "data" / "list_filtering.topydo.conf"

    def test_config_someday_projects(self):
        """Someday Project list from Config."""
        expected = [
            "have_yet_to_start",
            "someday_project",
        ]
        result = prjct.config.someday_projects(config_file=self.config_file)
        self.assertEqual(expected, result)

    def test_config_completed_projects(self):
        """Completed Project list from Config."""
        expected = ["completed_project"]
        result = prjct.config.completed_projects(config_file=self.config_file)
        self.assertEqual(expected, result)

    def test_config_all_projects(self):
        """All Project list from Config."""
        expected = [
            "completed_project",
            "have_yet_to_start",
            "someday_project",
        ]
        result = prjct.config.project_list(config_file=self.config_file)
        self.assertEqual(expected, result)

    def test_todo_all_projects(self):
        """All Projects list from Todo.txt."""
        expected = [
            "completed_project",
            "item",
            "ongoing_project",
            "prjct",
            "someday_project",
        ]
        result = prjct.todo_export.project_list(todo_cfg=self.todo_config_file)
        self.assertEqual(expected, result)

    def test_multi_source_all_projects(self):
        """All Projects from Multi-Source."""
        expected = [
            "completed_project",
            "have_yet_to_start",
            "item",
            "ongoing_project",
            "prjct",
            "someday_project",
        ]
        result = prjct.multi_source.project_list(config_file=self.config_file,
                                                 todo_config_file=self.todo_config_file)
        self.assertEqual(expected, result)

    def test_multi_source_active_projects(self):
        """Active Projects (only) from Multi-Source."""
        expected = [
            "item",
            "ongoing_project",
            "prjct",
        ]
        results = prjct.multi_source.active_project_list(config_file=self.config_file,
                                                         todo_config_file=self.todo_config_file)
        self.assertEqual(expected, results)


if __name__ == "__main__":
    unittest.main()
