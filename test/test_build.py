#! python

#  test_build.py: Test setup.py
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

"""usage: test_build.py

TEST CASES
  About                 Test the information about the app.
  LongDescription       Test the long description of the app.
"""

import os.path
import sys
import unittest

sys.path.insert(0, '..')

import setup
import test_contacts

__author__ = test_contacts.__author__
__version__ = test_contacts.__version__


class About(unittest.TestCase):
    """Test the information about the app.

    TESTS
      test_author       Test the contact details of the author.
      test_version      Test the version of the app.
    """

    def test_author(self):
        """Test the contact details of the author."""
        self.assertEqual(__author__, setup.__author__)

    def test_version(self):
        """Test the version of the app."""
        self.assertEqual(__version__, setup.__version__)


class LongDescription(unittest.TestCase):
    """Test the long description of the app.

    TEST
      test_readme       Test reading the README file.
    """

    def test_readme(self):
        """Test reading the README file."""
        with open(setup.README_FILE) as file:
            self.assertEqual(file.read(), setup.readme())


setup.README_FILE = os.path.join('..', 'README.txt')


if __name__ == '__main__':
    unittest.main()
