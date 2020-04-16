#! python

#  test_contacts.py: Test contacts.py
#  Copyright (C) 2020  Delvian Valentine <delvian.valentine@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""usage: test_contacts.py"""

import argparse
import os
import sys
import unittest

sys.path.insert(0, '..')

import contacts as package
from contacts import contacts


class Action(unittest.TestCase):

    """Test the actions.

    TESTS
      test_delete       Test deleting a contact.
      test_edit         Test editing a contact.
      test_new          Test creating a contact.
    """

    def setUp(self):
        """Create a command line parser for the tests."""
        self.parser = contacts.Parser()

    def test_delete(self):
        """Test deleting a contact."""
        self.parser.parse_args(['--new', 'name', 'email'])
        self.parser.parse_args(['--delete', 'name'])
        self.assertNotIn('name', contacts.load())

    def test_edit(self):
        """Test editing a contact."""
        self.parser.parse_args(['--new', 'name', 'none'])
        self.parser.parse_args(['--edit', 'name', 'email'])
        self.assertEqual('email', contacts.load()['name'])

    def test_new(self):
        """Test creating a contact."""
        self.parser.parse_args(['--new', 'name', 'email'])
        self.assertIn('name', contacts.load())

    def tearDown(self):
        """Delete the test file."""
        os.remove(contacts.FILE)


class Load(unittest.TestCase):

    """Test loading the contacts.

    TEST
      test_load         Test loading the contacts.
    """

    def test_load(self):
        """Test loading the contacts."""
        self.assertIsInstance(contacts.load(), dict)


class Parser(unittest.TestCase):

    """Test the command line parser.

    TESTS
      test_description  Test the description of the app.
      test_epilog       Test the epilog of the parser.
      test_formatter    Test the help formatter of the parser.
      test_help         Test the help message of the app.
      test_usage        Test the usage message of the app.
    """

    def setUp(self):
        """Create a parser to test."""
        self.parser = contacts.Parser()

    def test_description(self):
        """Test the description of the app."""
        self.assertEqual('Store your contacts.', self.parser.description)

    def test_epilog(self):
        """Test the epilog of the parser."""
        self.assertEqual(package.COPYRIGHT, self.parser.epilog)

    def test_formatter(self):
        """Test the help formatter of the parser."""
        self.assertIs(
            argparse.RawDescriptionHelpFormatter,
            self.parser.formatter_class
        )

    def test_help(self):
        """Test the help message of the app."""
        self.assertFalse(self.parser.add_help)

    def test_usage(self):
        """Test the usage message of the app."""
        self.assertEqual('%(prog)s [OPTIONS] [SEARCH]', self.parser.usage)


class Save(unittest.TestCase):

    """Test saving the contacts.

    TEST
      test_save         Test saving the contacts.
    """

    def test_save(self):
        """Test saving the contacts."""
        contacts.save({})
        self.assertTrue(os.path.exists(contacts.FILE))

    def tearDown(self):
        """Delete the test file."""
        os.remove(contacts.FILE)


class Search(unittest.TestCase):

    """Test searching the contacts.

    TEST
      test_search       Test searching the contacts.
    """

    def test_search(self):
        """Test searching the contacts."""
        self.assertEqual([], contacts.search(['search']))


class State(unittest.TestCase):

    """Test the state of the app."""

    def test_state(self):
        """Test the state of the app."""
        self.assertTrue(contacts.DEV_MODE)


# Store the contacts in a temporary file while testing the app.
contacts.FILE = '.test_contacts'

if __name__ == '__main__':
    unittest.main()
