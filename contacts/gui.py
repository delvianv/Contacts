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

import tkinter as tk
from tkinter import messagebox, ttk

import contacts


class App(tk.Tk):
    """The app"""

    def __init__(self):
        """Initialise the app."""
        super().__init__()
        self.title('Contacts')
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        try:
            self.contacts = contacts.load()
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while loading your contacts.',
                detail=err
            )
        self.filter = ''
        # The menubar
        self.option_add('*tearOff', tk.FALSE)
        menubar = tk.Menu(self)
        # The "Contact" menu
        menu_contact = tk.Menu(menubar)
        menu_contact.add_command(
            label='New',
            command=lambda: New(self)
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
        frame = ttk.Frame(self)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        # The tree
        self.tree = ttk.Treeview(frame, columns=['email'])
        self.tree.heading('#0', text='Full name')
        self.tree.heading('email', text='Email address')
        self.load()
        self.tree.grid(column=0, row=0, sticky='nsew')
        # The scrollbar
        scrollbar = ttk.Scrollbar(
            frame,
            orient='vertical',
            command=self.tree.yview
        )
        self.tree['yscrollcommand'] = scrollbar.set
        scrollbar.grid(column=1, row=0, sticky='ns')
        frame.grid(sticky='nsew')

    def delete(self):
        """Delete the selected contacts."""
        for item in self.tree.selection():
            del self.contacts[item]
            self.tree.delete(item)
        self.save()

    def load(self):
        """Load the contacts."""
        self.tree.delete(*self.tree.get_children())
        for name in sorted(
                contacts.search(self.filter, self.contacts) if self.filter
                else list(self.contacts)
        ):
            self.tree.insert(
                '',
                'end',
                name,
                text=name,
                values=[self.contacts[name]]
            )

    def open(self):
        """Open the selected contacts."""
        for item in self.tree.selection():
            Update(self, item)

    def save(self):
        """Save the contacts."""
        try:
            contacts.save(self.contacts)
        except OSError as err:
            messagebox.showerror(
                parent=self,
                message='There was an error while saving your contacts.',
                detail=err
            )
            self.quit()


class Contact(tk.Toplevel):
    """The 'Contact' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.resizable(tk.FALSE, tk.FALSE)
        self.name = tk.StringVar()
        self.email = tk.StringVar()
        # The frame
        frame = ttk.Frame(self, padding=12)
        # Labels
        ttk.Label(
            frame,
            text='Full name:'
        ).grid(column=0, row=0, sticky='w', pady=(0, 6))
        ttk.Label(
            frame,
            text='Email address:'
        ).grid(column=0, row=1, padx=(0, 6), pady=(0, 6))
        # Entries
        self.entry_name = ttk.Entry(
            frame,
            textvariable=self.name,
            width=30
        )
        self.entry_name.grid(column=1, row=0, pady=(0, 6))
        ttk.Entry(
            frame,
            textvariable=self.email,
            width=30
        ).grid(column=1, row=1, pady=(0, 6))
        # Buttons
        frame_buttons = ttk.Frame(frame)
        ttk.Button(
            frame_buttons,
            text='Cancel',
            command=self.destroy
        ).grid(column=0, row=0, padx=(0, 6))
        self.button_save = ttk.Button(
            frame_buttons,
            text='Save',
            command=self.save
        )
        self.button_save.grid(column=1, row=0)
        frame_buttons.grid(column=0, row=2, columnspan=2, sticky='e')
        frame.grid()

    def save(self):
        """Update the contacts."""
        self.master.contacts[self.name.get()] = self.email.get()
        self.master.save()
        self.master.load()
        self.destroy()


class Filter(tk.Toplevel):
    """The 'Filter' window"""

    def __init__(self, parent):
        """Initialise the window."""
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


class New(Contact):
    """The 'New Contact' window"""

    def __init__(self, parent):
        """Initialise the window."""
        super().__init__(parent)
        self.title('New Contact')
        validate = self.register(self.validate)
        self.entry_name['validate'] = 'all'
        self.entry_name['validatecommand'] = (validate, '%P')

    def validate(self, name):
        """Validate the name."""
        (self.button_save.state(['disabled']) if name in self.master.contacts
         else self.button_save.state(['!disabled']))
        return tk.TRUE


class Update(Contact):
    """The 'Update Contact' window"""

    def __init__(self, parent, name):
        """Initialise the window."""
        super().__init__(parent)
        self.title(name)
        self.name.set(name)
        self.email.set(self.master.contacts[name])
        self.entry_name.state(['readonly'])


def main():
    """Run the app."""
    App().mainloop()


if __name__ == '__main__':
    main()
