#  cli.py: The command line interface
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
"""usage: python -m contacts.cli"""

import argparse
import json
import os.path
import sys

FILE = '.contacts'


def delete(args):
    """Delete a contact."""
    contacts = load()
    if args.name in contacts:
        del contacts[args.name]
        save(contacts)
        print(f'{args.name} was deleted')
    else:
        print(f'{args.name} is not a contact.')


def edit(args):
    """Edit a contact."""
    contacts = load()
    if args.name in contacts:
        contacts[args.name] = args.email
        save(contacts)
        print(f'{args.name} was edited.')
    else:
        print(f'{args.name} is not a contact.')


def load():
    """Load the contacts."""
    if os.path.exists(FILE):
        try:
            with open(FILE) as file:
                return json.load(file)
        except OSError as err:
            print('There was an error while loading your contacts.')
            sys.exit(err)
    else:
        return {}


def main(argv=None):
    """Run the app."""
    # The command line parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # The "new" command parser
    parser_new = subparsers.add_parser('new')
    parser_new.add_argument('name')
    parser_new.add_argument('email')
    parser_new.set_defaults(command=new)
    # The "edit" command parser
    parser_edit = subparsers.add_parser('edit')
    parser_edit.add_argument('name')
    parser_edit.add_argument('email')
    parser_edit.set_defaults(command=edit)
    # The "delete" command parser
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('name')
    parser_delete.set_defaults(command=delete)
    # Parse the command line.
    args = parser.parse_args() if argv is None else parser.parse_args(argv)
    if 'command' in args:
        args.command(args)
    else:
        # Show the contacts if no command was given.
        for name in (contacts := load()):
            print(f'{name}: {contacts[name]}')


def new(args):
    """Store a new contact."""
    contacts = load()
    if args.name not in contacts:
        contacts[args.name] = args.email
        save(contacts)
        print(f'{args.name} was stored.')
    else:
        print(f'{args.name} is already a contact.')


def save(contacts):
    """Save the contacts."""
    try:
        with open(FILE, 'w') as file:
            json.dump(contacts, file)
    except OSError as err:
        print('There was an error while saving your contacts.')
        sys.exit(err)


if __name__ == '__main__':
    main()
