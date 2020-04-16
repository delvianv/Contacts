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

import contacts as package


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
        version=f'{package.__version__}',
        description=package.__doc__,
        long_description=readme(),
        long_description_content_type='text/markdown',
        url='https://pypi.org/project/Contacts/',
        author='Delvian Valentine',
        author_email='delvian.valentine@gmail.com',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Environment :: Console',
            'Environment :: MacOS X',
            'Environment :: Win32 (MS Windows)',
            'Environment :: X11 Applications',
            'Intended Audience :: End Users/Desktop',
            'License '
            ':: OSI Approved '
            ':: GNU General Public License v3 or later (GPLv3+)',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.8',
            'Topic :: Utilities'
        ],
        project_urls={'GitHub': 'https://github.com/delvianv/Contacts/'},
        keywords='contacts',
        packages=setuptools.find_packages(),
        python_requires='>=3.8',
        entry_points={
            'console_scripts': ['contacts=contacts.contacts:main'],
            'gui_scripts': ['contacts_gui=contacts.gui:main']
        }
    )
