#  gui.py: The graphical user interface
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
"""usage: python -m contacts.gui"""

import os.path
import tkinter as tk
from tkinter import ttk

import contacts


# class About(tk.Toplevel):
#
#     """The About Contacts window"""
#
#     def __init__(self, parent):
#         super().__init__(parent)
#         # Window
#         self.title('About Contacts')
#         # Frame
#         frame = ttk.Frame(self)
#         # Labels
#         ttk.Label(
#             frame,
#             text=f'Contacts {package.__version__}'
#         ).grid(column=0, row=0)
#         ttk.Label(frame, text=package.__doc__).grid(column=0, row=1)
#         ttk.Label(frame, text=package.COPYRIGHT).grid(column=0, row=2)
#         # Close button
#         ttk.Button(
#             frame,
#             text='Close',
#             command=self.destroy
#         ).grid(column=0, row=3)
#         frame.grid()
#
#
# class Contact(tk.Toplevel):
#
#     """The Contact window"""
#
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.name = tk.StringVar()
#         self.email = tk.StringVar()
#         # Frame
#         frame = ttk.Frame(self)
#         # Labels
#         ttk.Label(frame, text='Full name:').grid(column=0, row=0)
#         ttk.Label(frame, text='Email address:').grid(column=0, row=1)
#         # Entries
#         ttk.Entry(frame, textvariable=self.name).grid(column=1, row=0)
#         ttk.Entry(frame, textvariable=self.email).grid(column=1, row=1)
#         # Buttons
#         buttons_frame = ttk.Frame(frame)
#         ttk.Button(
#             buttons_frame,
#             text='Cancel',
#             command=self.destroy
#         ).grid(column=0, row=0)
#         ttk.Button(
#             buttons_frame,
#             text='Save',
#             command=self.save
#         ).grid(column=1, row=0)
#         buttons_frame.grid(column=0, row=2, columnspan=2)
#         frame.grid()
#
#     def save(self):
#         """Save the contact."""
#
#
# class Filter(tk.Toplevel):
#
#     """The Filter window"""
#
#     def __init__(self, parent, search):
#         super().__init__(parent)
#         self.response = False
#         self.search = tk.StringVar()
#         self.search.set(search)
#         # Window
#         self.title('Filter')
#         # Frame
#         frame = ttk.Frame(self)
#         # Label
#         ttk.Label(frame, text='Filter:').grid(column=0, row=0)
#         # Entry
#         ttk.Entry(frame, textvariable=self.search).grid(column=1, row=0)
#         # Buttons
#         buttons_frame = ttk.Frame(frame)
#         ttk.Button(
#             buttons_frame,
#             text='Cancel',
#             command=self.destroy
#         ).grid(column=0, row=0)
#         ttk.Button(
#             buttons_frame,
#             text='Filter',
#             command=self.filter
#         ).grid(column=1, row=0)
#         buttons_frame.grid(column=0, row=1, columnspan=2)
#         frame.grid()
#
#     def filter(self):
#         """Filter the contacts."""
#         self.response = True
#         self.destroy()
#
#     def wait(self):
#         """Wait for the window to close."""
#         self.wait_window(self)
#         if self.response:
#             return self.search.get()
#
#
# class GUI(tk.Tk):
#
#     """The graphical user interface"""
#
#     def __init__(self):
#         super().__init__()
#         self.mtime = 0
#         self.tree = None
#         self.search = ''
#         # Window
#         self.title('Contacts')
#         self.bind('<FocusIn>', lambda e: self.reload())
#         # Menubar
#         self.option_add('*tearOff', tk.FALSE)
#         menubar = tk.Menu(self)
#         # Contact menu
#         contact_menu = tk.Menu(menubar)
#         contact_menu.add_command(label='New', command=lambda: New(self))
#         contact_menu.add_command(label='Open', command=self.open)
#         contact_menu.add_command(label='Delete', command=self.delete)
#         contact_menu.add_separator()
#         contact_menu.add_command(label='Filter...', command=self.filter)
#         contact_menu.add_separator()
#         contact_menu.add_command(label='Quit', command=self.quit)
#         menubar.add_cascade(menu=contact_menu, label='Contact')
#         # Help menu
#         help_menu = tk.Menu(menubar)
#         help_menu.add_command(label='About', command=lambda: About(self))
#         menubar.add_cascade(menu=help_menu, label='Help')
#         self['menu'] = menubar
#         self.mainloop()
#
#     def delete(self):
#         """Delete the contacts that are selected."""
#         for item in self.tree.selection():
#             contacts.Parser().parse_args(
#                 ['--delete', self.tree.item(item, 'text')]
#             )
#         self.reload()
#
#     def filter(self):
#         """Filter the contacts."""
#         if (response := Filter(self, self.search).wait()) is not None:
#             self.search = response
#             self.load()
#
#     def load(self):
#         """Load the contacts."""
#         # Frame
#         frame = ttk.Frame(self)
#         # Tree
#         self.tree = ttk.Treeview(frame, columns=['email'])
#         self.tree.heading('#0', text='Full name')
#         self.tree.heading('email', text='Email address')
#         search = self.search
#         people = contacts.load()
#         names = contacts.search(search.split()) if search else list(people)
#         for name in sorted(names):
#             self.tree.insert('', 'end', text=name, values=[people[name]])
#         self.tree.grid()
#         frame.grid(column=0, row=0)
#
#     def open(self):
#         """Open the contacts that are selected."""
#         for item in self.tree.selection():
#             Open(self, self.tree.item(item, 'text'))
#
#     def reload(self):
#         """Reload the contacts if the file was updated."""
#         if os.path.exists(package.CONTACTS_FILE):
#            if (mtime := os.path.getmtime(package.CONTACTS_FILE)) > self.mtime:
#                 self.load()
#                 self.mtime = mtime
#         else:
#             self.load()
#
#
# class New(Contact):
#
#     """The New Contact window"""
#
#     def __init__(self, parent):
#         super().__init__(parent)
#         # Window
#         self.title('New Contact')
#
#     def save(self):
#         """Save the contact."""
#         contacts.Parser().parse_args(
#             ['--new', self.name.get(), self.email.get()]
#         )
#         self.destroy()
#
#
# class Open(Contact):
#
#     """The Open Contact window"""
#
#     def __init__(self, parent, name):
#         super().__init__(parent)
#         self.name.set(name)
#         self.email.set(contacts.load()[name])
#         # Window
#         self.title(name)
#
#     def save(self):
#         """Save the contact."""
#         contacts.Parser().parse_args(
#             ['--edit', self.name.get(), self.email.get()]
#         )
#         self.destroy()


class App(tk.Tk):
    """The app"""

    def __init__(self):
        """Initialise the app."""
        super().__init__()
        self.people = {}
        self.mtime = 0
        self.filter = ''
        # Events
        self.bind('<FocusIn>', lambda e: self.reload())
        # The menubar
        self.option_add('*tearOff', tk.FALSE)
        menubar = tk.Menu(self)
        # The "Contact" menu
        menu_contact = tk.Menu(menubar)
        menu_contact.add_command(
            label='New',
            command=lambda: Contact(self)
        )
        menu_contact.add_command(label='Open', command=self.open)
        menu_contact.add_command(label='Delete', command=self.delete)
        menu_contact.add_command(
            label='Filter...',
            command=lambda: Filter(self)
        )
        menubar.add_cascade(menu=menu_contact, label='Contact')
        self['menu'] = menubar
        # The frame
        self.frame = ttk.Frame(self)
        # The tree
        self.tree = ttk.Treeview(self.frame)
        self.load()
        self.frame.grid()

    def delete(self):
        """Delete the selected contacts."""
        for item in self.tree.selection():
            del self.people[self.tree.item(item, 'text')]
        contacts.save(self.people)
        self.load()

    def load(self):
        """Load the contacts."""
        self.people = contacts.load()
        # The tree
        self.tree = ttk.Treeview(self.frame, columns=['email'])
        if self.filter:
            names = contacts.search(self.filter, self.people)
        else:
            names = list(self.people)
        for name in names:
            self.tree.insert(
                '',
                'end',
                text=name,
                values=[self.people[name]]
            )
        self.tree.grid(column=0, row=0)

    def open(self):
        """Open the selected contacts."""
        for item in self.tree.selection():
            Contact(self, self.tree.item(item, 'text'))

    def reload(self):
        """Reload the contacts."""
        if os.path.exists(contacts.FILE):
            if (mtime := os.path.getmtime(contacts.FILE)) > self.mtime:
                self.load()
                self.mtime = mtime


class Contact(tk.Toplevel):
    """The 'Contact' window"""

    def __init__(self, parent, name=None):
        """Initialise the 'Contact' window."""
        super().__init__(parent)
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        if name is not None:
            self.name.set(name)
            self.email.set(parent.people[name])
        # The frame
        frame = ttk.Frame(self)
        # Labels
        ttk.Label(self, text='Name:').grid(column=0, row=0)
        ttk.Label(self, text='Email:').grid(column=0, row=1)
        # Entries
        ttk.Entry(self, textvariable=self.name).grid(column=1, row=0)
        ttk.Entry(self, textvariable=self.email).grid(column=1, row=1)
        # The button
        ttk.Button(self, text='Save', command=self.save).grid(column=1, row=2)
        frame.grid()

    def save(self):
        """Update the contact."""
        self.master.people[self.name.get()] = self.email.get()
        contacts.save(self.master.people)
        self.destroy()


class Filter(tk.Toplevel):
    """The 'Filter' window"""

    def __init__(self, parent):
        """Initialise the 'Filter' window."""
        super().__init__(parent)
        self.search = tk.StringVar()
        self.search.set(parent.filter)
        # The frame
        frame = ttk.Frame(self)
        # The label
        ttk.Label(frame, text='Filter:').grid(column=0, row=0)
        # The entry
        ttk.Entry(frame, textvariable=self.search).grid(column=1, row=0)
        # The button
        ttk.Button(
            frame,
            text='Filter',
            command=self.filter
        ).grid(column=1, row=1)
        frame.grid()

    def filter(self):
        """Filter the contacts."""
        self.master.filter = self.search.get()
        self.master.load()
        self.destroy()


def main():
    """Run the app."""
    App().mainloop()


if __name__ == '__main__':
    main()
