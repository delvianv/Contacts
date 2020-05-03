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
from tkinter import messagebox, ttk

import contacts


class App(tk.Tk):
    """The app"""

    def __init__(self):
        """Initialise the app."""
        super().__init__()
        self.people = {}
        self.filter = ''
        self.mtime = 0
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
        menu_contact.add_command(
            label='Open',
            command=self.open
        )
        menu_contact.add_command(
            label='Delete',
            command=self.delete
        )
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
        self.save()
        self.load()

    def load(self):
        """Load the contacts."""
        try:
            self.people = contacts.load()
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while loading your contacts.',
                detail=err
            )
            self.quit()
        # The tree
        self.tree = ttk.Treeview(self.frame, columns=['email'])
        names = (
            contacts.search(self.filter, self.people) if self.filter
            else list(self.people)
        )
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
            try:
                if (mtime := os.path.getmtime(contacts.FILE)) > self.mtime:
                    self.load()
                    self.mtime = mtime
            except OSError as err:
                messagebox.showerror(
                    parent=self,
                    message='There was an error while reloading your contacts.',
                    detail=err
                )
                self.quit()

    def save(self):
        """Save the contacts."""
        try:
            contacts.save(self.people)
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while saving your contacts.',
                detail=err
            )
            self.quit()


class Contact(tk.Toplevel):
    """The 'Contact' window"""

    def __init__(self, parent, name=None):
        """Initialise the 'Contact' window."""
        super().__init__(parent)
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        if name is not None:
            self.name.set(name)
            self.email.set(self.master.people[name])
        # The frame
        frame = ttk.Frame(self)
        # Labels
        ttk.Label(self, text='Name:').grid(column=0, row=0)
        ttk.Label(self, text='Email:').grid(column=0, row=1)
        # Entries
        ttk.Entry(self, textvariable=self.name).grid(column=1, row=0)
        ttk.Entry(self, textvariable=self.email).grid(column=1, row=1)
        # The button
        ttk.Button(
            self,
            text='Save',
            command=self.save
        ).grid(column=0, row=2, columnspan=2)
        frame.grid()

    def save(self):
        """Update the contact."""
        self.master.people[self.name.get()] = self.email.get()
        self.master.save()
        self.destroy()


class Filter(tk.Toplevel):
    """The 'Filter' window"""

    def __init__(self, parent):
        """Initialise the 'Filter' window."""
        super().__init__(parent)
        self.search = tk.StringVar()
        self.search.set(self.master.filter)
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
