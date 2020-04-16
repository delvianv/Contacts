#  contacts.py: The command line interface
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

"""usage: contacts [OPTIONS] [SEARCH]

Store your contacts.

positional arguments:
  SEARCH             search your contacts

optional arguments:
  --new NAME EMAIL   create a contact
  --edit NAME EMAIL  edit a contact
  --delete NAME      delete a contact
  --help             show this message
  --version          show the version of the app
"""

import argparse
import json
import os.path
import sys

import contacts as package


class Delete(argparse.Action):

    """Delete a contact."""

    def __call__(self, parser, namespace, name, option_string=None):
        if name in (contacts := load()):
            del contacts[name]
            save(contacts)
            print(f'{name} was deleted.')
        else:
            print(f'{name} is not a contact.')


class Edit(argparse.Action):

    """Edit a contact."""

    def __call__(self, parser, namespace, values, option_string=None):
        name, email = values
        if name in (contacts := load()):
            contacts[name] = email
            save(contacts)
            print(f'{name} was edited.')
        else:
            print(f'{name} is not a contact.')


class New(argparse.Action):

    """Create a contact."""

    def __call__(self, parser, namespace, values, option_string=None):
        name, email = values
        if name not in (contacts := load()):
            contacts[name] = email
            save(contacts)
            print(f'{name} was created.')
        else:
            print(f'{name} is already a contact.')


class Parser(argparse.ArgumentParser):

    """The command line parser"""

    # noinspection PyTypeChecker
    def __init__(self):
        super().__init__(
            usage='%(prog)s [OPTIONS] [SEARCH]',
            description=package.__doc__,
            epilog=package.COPYRIGHT,
            formatter_class=argparse.RawDescriptionHelpFormatter,
            add_help=False
        )
        self.add_argument(
            'search',
            nargs='*',
            help='search your contacts',
            metavar='SEARCH'
        )
        self.add_argument(
            '--new',
            action=New,
            nargs=2,
            help='create a contact',
            metavar=('NAME', 'EMAIL')
        )
        self.add_argument(
            '--edit',
            action=Edit,
            nargs=2,
            help='edit a contact',
            metavar=('NAME', 'EMAIL')
        )
        self.add_argument(
            '--delete',
            action=Delete,
            help='delete a contact',
            metavar='NAME'
        )
        self.add_argument('--help', action='help', help='show this message')
        self.add_argument(
            '--version',
            action='version',
            version=f'{package.__version__}',
            help='show the version of the app'
        )


def load():
    """Load the contacts.

    Exit the app if there was an error.

    Return the contacts or an empty dictionary if there are no contacts.
    """
    if os.path.exists(package.CONTACTS_FILE):
        try:
            with open(package.CONTACTS_FILE) as file:
                return json.load(file)
        except OSError as err:
            print('There was an error while loading your contacts.')
            sys.exit(err)
    else:
        return {}


def print_(names):
    """Print the contacts.

    ARGUMENT
      names             A list of contacts to print.
    """
    contacts = load()
    for name in sorted(names):
        print(f'{name}: {contacts[name]}')


def save(contacts):
    """Save the contacts.

    ARGUMENT
      contacts          The contacts to save.

    Exit the app if there was an error.
    """
    try:
        with open(package.CONTACTS_FILE, 'w') as file:
            json.dump(contacts, file)
    except OSError as err:
        print('There was an error while saving your contacts.')
        sys.exit(err)


def search(terms):
    """Search the contacts.

    ARGUMENT
      terms            A list of terms to search for.

    Return a list of contacts that match the search.
    """
    results = []
    for name in (contacts := load()):
        for term in terms:
            if term not in name and term not in contacts[name]:
                break
        else:
            results.append(name)
    return results


def show(names=None):
    """Show the contacts.

    ARGUMENT
      names             A list of contacts to show.
    """
    if names is not None:
        # Only show the named contacts.
        if names:
            print_(names)
        else:
            print('None of your contacts match your search.')
    else:
        # Show all of the contacts.
        if contacts := load():
            print_(list(contacts))
        else:
            print('You do not have any contacts.')


def main():
    """Run the app."""
    args = Parser().parse_args()
    if args.search:
        # Search the contacts if there are search terms on the command line.
        show(search(args.search))
    if not sys.argv[1:]:
        # Show the contacts if there are no arguments on the command line.
        show()


if __name__ == '__main__':
    main()
