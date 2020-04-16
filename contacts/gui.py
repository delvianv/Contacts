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

import tkinter as tk
from tkinter import ttk

import contacts as package
from contacts import contacts


class About(tk.Toplevel):

    """The About window"""

    def __init__(self, parent):
        super().__init__(parent)
        # Window
        self.title('About Contacts')
        # Frame
        frame = ttk.Frame(self)
        # Labels
        ttk.Label(
            frame,
            text=f'Contacts {package.__version__}'
        ).grid(column=0, row=0)
        ttk.Label(frame, text=package.__doc__).grid(column=0, row=1)
        ttk.Label(frame, text=package.COPYRIGHT).grid(column=0, row=2)
        # Close button
        ttk.Button(
            frame,
            text='Close',
            command=self.destroy
        ).grid(column=0, row=3)
        frame.grid()


class GUI(tk.Tk):

    """The graphical user interface"""

    def __init__(self):
        super().__init__()
        # Window
        self.title('Contacts')
        # Menubar
        self.option_add('*tearOff', tk.FALSE)
        menubar = tk.Menu(self)
        # Contact menu
        contact_menu = tk.Menu(menubar)
        contact_menu.add_command(label='Quit', command=self.quit)
        menubar.add_cascade(menu=contact_menu, label='Contact')
        # Help menu
        help_menu = tk.Menu(menubar)
        help_menu.add_command(label='About', command=lambda: About(self))
        menubar.add_cascade(menu=help_menu, label='Help')
        self['menu'] = menubar
        # Frame
        frame = ttk.Frame(self)
        # Tree
        tree = ttk.Treeview(frame, columns=['email'])
        tree.heading('#0', text='Full name')
        tree.heading('email', text='Email address')
        for name in sorted(people := contacts.load()):
            tree.insert('', 'end', text=name, values=[people[name]])
        tree.grid()
        frame.grid()
        self.mainloop()


def main():
    """Run the app."""
    GUI()


if __name__ == '__main__':
    main()
