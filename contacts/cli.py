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
import sys

import contacts

COPYRIGHT = f'''Copyright (C) 2020  {contacts.__author__}
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it under
certain conditions.  See the GNU General Public License for more
details <https://www.gnu.org/licenses/>.'''


def delete(args):
    """Delete contacts."""
    people = load()
    modified = False
    # Delete the named contacts.
    names = (
        contacts.search(args.search, people) if args.search else args.names
    )
    for name in names:
        try:
            del people[name]
        except KeyError:
            print(f'{name} is not a contact.')
        else:
            modified = True
            print(f'{name} was deleted.')
    # Delete all the contacts.
    if args.all:
        people.clear()
        modified = True
        print('All your contacts were deleted.')
    if modified:
        save(people)


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
    parser.add_argument(
        '--search',
        help='show your contacts that match the search'
    )
    parser.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
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
        usage='new [OPTION] name email',
        description='Store a new contact.',
        help='store a new contact',
        add_help=False
    )
    parser_new.add_argument(
        'name',
        help='the name of the contact'
    )
    parser_new.add_argument(
        'email',
        help='the email address of the contact'
    )
    parser_new.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
    parser_new.set_defaults(command=new)
    # The "update" command parser
    parser_update = subparsers.add_parser(
        'update',
        usage='update [OPTION] name email',
        description='Update a contact.',
        help='update a contact',
        add_help=False
    )
    parser_update.add_argument(
        'name',
        help='the name of the contact'
    )
    parser_update.add_argument(
        'email',
        help='the email address of the contact'
    )
    parser_update.add_argument(
        '-h',
        '--help',
        action='help',
        help='show this message'
    )
    parser_update.set_defaults(command=update)
    # The "delete" command parser
    parser_delete = subparsers.add_parser(
        'delete',
        aliases=['del'],
        usage='delete [OPTION] [names]',
        description='Delete your contacts.',
        help='delete your contacts',
        add_help=False
    )
    parser_delete.add_argument(
        'names',
        nargs='*',
        help='the names of your contacts'
    )
    parser_delete_group = parser_delete.add_mutually_exclusive_group()
    parser_delete_group.add_argument(
        '--search',
        help='delete your contacts that match the search'
    )
    parser_delete_group.add_argument(
        '--all',
        action='store_true',
        help='delete all your contacts'
    )
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
        names = (
            contacts.search(args.search, people) if args.search
            else list(people)
        )
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


def save(people):
    """Save the contacts."""
    try:
        contacts.save(people)
    except OSError as err:
        print('There was an error while saving your contacts.')
        sys.exit(err)


def update(args):
    """Update a contact."""
    people = load()
    if args.name in people:
        people[args.name] = args.email
        save(people)
        print(f'{args.name} was updated.')
    else:
        print(f'{args.name} is not a contact.')


if __name__ == '__main__':
    main()
