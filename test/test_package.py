#  test_package.py: Test __init__.py
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

__author__ = 'Delvian Valentine <delvian.valentine@gmail.com>'
__version__ = '2.0.dev8'

import os.path
import unittest

import contacts as package


class About(unittest.TestCase):

    """Test the information about the app.

    TESTS
      test_author       Test the contact details of the author.
      test_description  Test the description of the app.
      test_version      Test the version of the app.
    """

    def test_author(self):
        """Test the contact details of the author."""
        self.assertEqual(__author__, package.__author__)

    def test_copyright(self):
        """Test the copyright of the app."""
        self.assertEqual(COPYRIGHT, package.COPYRIGHT)

    def test_description(self):
        """Test the description of the app."""
        self.assertEqual('Store your contacts.', package.__doc__)

    def test_version(self):
        """Test the version of the app."""
        self.assertEqual(__version__, package.__version__)


class State(unittest.TestCase):

    """Test the state of the app.

    TEST
      test_state        Test the state of the app.
    """

    def test_state(self):
        """Test the state of the app."""
        self.assertTrue(package.DEV_MODE)


COPYRIGHT = f'''Copyright (C) 2020  {__author__}
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under
certain conditions.  See the GNU General Public License for more
details <https://www.gnu.org/licenses/>.'''

if __name__ == '__main__':
    unittest.main()
