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

FILE = '.contacts'


def delete(args):
    """Delete a contact."""
    contacts = load()
    del contacts[args.name]
    save(contacts)


def load():
    """Load the contacts."""
    if os.path.exists(FILE):
        with open(FILE) as file:
            return json.load(file)
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
    contacts[args.name] = args.email
    save(contacts)


def save(contacts):
    """Save the contacts."""
    with open(FILE, 'w') as file:
        json.dump(contacts, file)


if __name__ == '__main__':
    main()
