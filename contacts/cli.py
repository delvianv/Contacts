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
"""usage: python -m contacts.cli [OPTION] {COMMAND}"""

import argparse
import json
import sys

import contacts

COPYRIGHT = f'''Copyright (C) 2020  {contacts.__author__}
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under
certain conditions.  See the GNU General Public License for more
details <https://www.gnu.org/licenses/>.'''
FILE_CONTACTS = '.contacts'


def delete(args):
    """Delete a contact."""
    people = load()
    if args.name in people:
        del people[args.name]
        save(people)
        print(f'{args.name} was deleted')
    else:
        print(f'{args.name} is not a contact.')


def edit(args):
    """Edit a contact."""
    people = load()
    if args.name in people:
        people[args.name] = args.email
        save(people)
        print(f'{args.name} was edited.')
    else:
        print(f'{args.name} is not a contact.')


def load():
    """Load the contacts."""
    try:
        return contacts.load()
    except OSError as err:
        print('There was an error while loading your contacts.')
        sys.exit(err)


def main(argv=None):
    """Run the app."""
    # The command line parser
    # noinspection PyTypeChecker
    parser = argparse.ArgumentParser(
        usage='%(prog)s [OPTION] {COMMAND}',
        description='Show your contacts.',
        epilog=COPYRIGHT,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
    )
    parser.add_argument('--search', help='search your contacts')
    parser.add_argument('-h', '--help', action='help', help='show this message')
    parser.add_argument(
        '--version',
        action='version',
        version=contacts.__version__,
        help='show the version of the app'
    )
    subparsers = parser.add_subparsers(
        description='Update your contacts.',
        metavar='{COMMAND}'
    )
    # The "new" command parser
    parser_new = subparsers.add_parser(
        'new',
        usage='new [-h] name email',
        description='Store a new contact.',
        help='store a new contact',
        add_help=False
    )
    parser_new.add_argument('name', help='the name of the contact')
    parser_new.add_argument('email', help='the email address of the contact')
    parser_new.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
    parser_new.set_defaults(command=new)
    # The "edit" command parser
    parser_edit = subparsers.add_parser(
        'edit',
        usage='edit [-h] name email',
        description='Edit a contact.',
        help='edit a contact',
        add_help=False
    )
    parser_edit.add_argument('name', help='the name of the contact')
    parser_edit.add_argument('email', help='the email address of the contact')
    parser_edit.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
    parser_edit.set_defaults(command=edit)
    # The "delete" command parser
    parser_delete = subparsers.add_parser(
        'delete',
        usage='delete [-h] name',
        description='Delete a contact.',
        help='delete a contact',
        add_help=False
    )
    parser_delete.add_argument('name', help='the name of the contact')
    parser_delete.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
    parser_delete.set_defaults(command=delete)
    # Parse the command line.
    args = parser.parse_args() if argv is None else parser.parse_args(argv)
    if 'command' in args:
        # Update the contacts.
        args.command(args)
    else:
        # Show the contacts.
        people = load()
        names = search(args.search, people) if args.search else list(people)
        if names:
            for name in sorted(names):
                print(f'{name}: {people[name]}')
        else:
            print('There are no contacts to show.')


def new(args):
    """Store a new contact."""
    people = load()
    if args.name not in people:
        people[args.name] = args.email
        save(people)
        print(f'{args.name} was stored.')
    else:
        print(f'{args.name} is already a contact.')


def search(arg, people):
    """Search the contacts."""
    names = []
    for name in people:
        if arg in name or arg in people[name]:
            names.append(name)
    return names


def save(people):
    """Save the contacts."""
    try:
        with open(FILE_CONTACTS, 'w') as file:
            json.dump(people, file)
    except OSError as err:
        print('There was an error while saving your contacts.')
        sys.exit(err)


if __name__ == '__main__':
    main()
