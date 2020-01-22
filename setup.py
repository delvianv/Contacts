#! python

#  setup.py: Build/install the app.
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

"""usage: setup.py build|install"""

import setuptools
import sys

import contacts

__author__ = contacts.__author__
__version__ = contacts.__version__


def readme():
    """Read the README file.

    Return the README file.
    """
    try:
        with open(README_FILE) as file:
            return file.read()
    except OSError as err:
        print(f'There was an error while opening {README_FILE}')
        sys.exit(err)


README_FILE = 'README.txt'


if __name__ == '__main__':
    setuptools.setup(
        name='Contacts',
        version=f'{__version__}',
        description='Manage your contacts.',
        long_description=readme(),
        long_description_content_type='text/x-rst',
        author='Delvian Valentine',
        author_email='delvian.valentine@gmail.com',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: '
            'GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.7',
            'Topic :: Utilities'
        ],
        keywords='contacts',
        py_modules=['contacts'],
        python_requires='>=3.7',
        entry_points={
            'console_scripts': ['contacts=contacts:main']
        }
    )
