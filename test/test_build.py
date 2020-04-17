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

"""usage: test_build.py"""

import os.path
import sys
import unittest

sys.path.insert(0, '..')

import setup


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
