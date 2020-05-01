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

FILE = '.contacts'


def load():
    """Load the contacts."""
    with open(FILE) as file:
        return json.load(file)


def main():
    """Run the app."""
    # The command line parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    # The "new" command parser
    parser_new = subparsers.add_parser('new')
    parser_new.add_argument('name')
    parser_new.add_argument('email')
    parser_new.set_defaults(command=new)
    # Parse the command line.
    args = parser.parse_args()
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
    with open(FILE, 'w') as file:
        json.dump(contacts, file)


if __name__ == '__main__':
    main()
