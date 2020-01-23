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

"""usage: test_contacts.py

TEST CASES
  About                 Test the information about the app.
  Action                Test the actions.
  Load                  Test loading the contacts.
  Parser                Test the command line parser.
  Save                  Test saving the contacts.
  Search                Test searching the contacts.
"""

import argparse
import os
import sys
import unittest

sys.path.insert(0, '..')

import contacts

__author__ = 'Delvian Valentine <delvian.valentine@gmail.com>'
__version__ = '0.2.4'


class About(unittest.TestCase):
    """Test the information about the app.

    TESTS
      test_author       Test the contact details of the author.
      test_version      Test the version of the app.
    """

    def test_author(self):
        """Test the contact details of the author."""
        self.assertEqual(__author__, contacts.__author__)

    def test_version(self):
        """Test the version of the app."""
        self.assertEqual(__version__, contacts.__version__)


class Action(unittest.TestCase):
    """Test the actions.

    TESTS
      setUp             Create a command line parser for the tests.
      test_delete       Test deleting a contact.
      test_edit         Test editing a contact.
      test_new          Test creating a contact.
      tearDown          Delete the test file.
    """

    def setUp(self):
        """Create a command line parser for the tests."""
        self.parser = contacts.Parser()

    def test_delete(self):
        """Test deleting a contact."""
        self.parser.parse_args(['--new', 'name', 'email'])
        self.parser.parse_args(['--delete', 'name'])
        self.assertNotIn('name', contacts.load_contacts())

    def test_edit(self):
        """Test editing a contact."""
        self.parser.parse_args(['--new', 'name', 'none'])
        self.parser.parse_args(['--edit', 'name', 'email'])
        self.assertEqual('email', contacts.load_contacts()['name'])

    def test_new(self):
        """Test creating a contact."""
        self.parser.parse_args(['--new', 'name', 'email'])
        self.assertIn('name', contacts.load_contacts())

    def tearDown(self):
        """Delete the test file."""
        os.remove(contacts.CONTACTS_FILE)


class File(unittest.TestCase):
    """Test the name of the contacts file.

    TEST
      test_file         Test the name of the contacts file.
    """

    def test_file(self):
        """Test the name of the contacts file."""
        self.assertEqual('.test_contacts', contacts.CONTACTS_FILE)


class Load(unittest.TestCase):
    """Test loading the contacts.

    TEST
      test_load         Test loading the contacts.
    """

    def test_load(self):
        """Test loading the contacts."""
        self.assertIsInstance(contacts.load_contacts(), dict)


class Parser(unittest.TestCase):
    """Test the command line parser.

    TESTS
      setUp             Create a parser to test.
      test_description  Test the description of the app.
      test_epilog       Test the epilog of the app.
      test_formatter    Test the help formatter of the app.
      test_help         Test the help message of the app.
      test_usage        Test the usage message of the app.
    """

    def setUp(self):
        """Create a parser to test."""
        self.parser = contacts.Parser()

    def test_description(self):
        """Test the description of the app."""
        self.assertEqual('Manage your contacts.', self.parser.description)

    def test_epilog(self):
        """Test the epilog of the app."""
        self.assertEqual(COPYRIGHT, self.parser.epilog)

    def test_formatter(self):
        """Test the help formatter of the app."""
        self.assertIs(
            argparse.RawDescriptionHelpFormatter,
            self.parser.formatter_class
        )

    def test_help(self):
        """Test the help message of the app."""
        self.assertFalse(self.parser.add_help)

    def test_usage(self):
        """Test the usage of the app."""
        self.assertEqual('%(prog)s [OPTIONS] [SEARCH]', self.parser.usage)


class Save(unittest.TestCase):
    """Test saving the contacts.

    TESTS
      test_save         Test saving the contacts.
      tearDown          Delete the test file.
    """

    def test_save(self):
        """Test saving the contacts."""
        contacts.save_contacts({})
        self.assertTrue(os.path.exists(contacts.CONTACTS_FILE))

    def tearDown(self):
        """Delete the test file."""
        os.remove(contacts.CONTACTS_FILE)


class Search(unittest.TestCase):
    """Test searching the contacts.

    TESTS
      test_search       Test searching the contacts.
    """

    def test_search(self):
        """Test searching the contacts."""
        self.assertEqual([], contacts.search_contacts(['search']))


contacts.CONTACTS_FILE = '.test_contacts'
COPYRIGHT = f'''Copyright (C) 2020  {__author__}
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under
certain conditions.  See the GNU General Public License for more
details <https://www.gnu.org/licenses/>.'''

if __name__ == '__main__':
    unittest.main()
