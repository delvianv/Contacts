#! python

#  test_cli.py: Test the command line interface.
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
"""usage: test_cli.py"""

__author__ = 'Delvian Valentine <delvian.valentine@gmail.com>'
__version__ = '2.0'

import os
import sys
import unittest

sys.path.insert(0, '..')

from contacts import cli

FILE = '.contacts'


class Delete(unittest.TestCase):
    """Delete a contact."""

    def setUp(self):
        """Delete a contact."""
        cli.main(['new', 'name', 'email'])
        cli.main(['delete', 'name'])

    def test_delete(self):
        """Test deleting a contact."""
        self.assertEqual(cli.load(), {})

    def tearDown(self):
        """Remove the file."""
        os.remove(FILE)


class Edit(unittest.TestCase):
    """Edit a contact."""

    def setUp(self):
        """Edit a contact."""
        cli.main(['new', 'name', 'email'])
        cli.main(['edit', 'name', '@'])

    def test_edit(self):
        """Test editing a contact."""
        self.assertEqual(cli.load(), {'name': '@'})

    def tearDown(self):
        """Remove the file."""
        os.remove(FILE)


class Load(unittest.TestCase):
    """Load the contacts."""

    def test_load(self):
        """Test loading the contacts."""
        self.assertEqual(cli.load(), {})


class New(unittest.TestCase):
    """Store a new contact."""

    def setUp(self):
        """Store a new contact."""
        cli.main(['new', 'name', 'email'])

    def test_new(self):
        """Test storing a new contact."""
        self.assertEqual(cli.load(), {'name': 'email'})

    def tearDown(self):
        """Remove the file."""
        os.remove(FILE)


class Save(unittest.TestCase):
    """Save the contacts."""

    def setUp(self):
        """Save the contacts."""
        self.contacts = {'name': 'email'}
        cli.save(self.contacts)

    def test_save(self):
        """Test saving the contacts."""
        self.assertEqual(cli.load(), self.contacts)

    def tearDown(self):
        """Remove the file."""
        os.remove(FILE)


class Search(unittest.TestCase):
    """Search the contacts."""

    def test_search(self):
        """Test searching the contacts."""
        self.assertEqual(cli.search('name', {'name': 'email'}), ['name'])


if __name__ == '__main__':
    unittest.main()
