#!/usr/bin/env python

# example helloworld.py
import subprocess

import pygtk

pygtk.require('2.0')
import gtk


class TextEntry(gtk.Entry):
    def __init__(self, window):
        gtk.Entry.__init__(self)
        self.keyboard = window.keyboard

        self.connect("focus-in-event", self.on_focus_in)
        self.connect("focus-out-event", self.on_focus_out)

    def on_focus_in(self, event, data):
        self.keyboard.show()

    def on_focus_out(self, event, data):
        self.keyboard.hide()


class HelloWorld:
    # This is a callback function. The data arguments are ignored
    # in this example. More on callbacks below.
    def hello(self, widget, data=None):
        print "Hello World"

    def delete_event(self, widget, event, data=None):
        # If you return FALSE in the "delete_event" signal handler,
        # GTK will emit the "destroy" signal. Returning TRUE means
        # you don't want the window to be destroyed.
        # This is useful for popping up 'are you sure you want to quit?'
        # type dialogs.
        print "delete event occurred"

        # Change FALSE to TRUE and the main window will not be destroyed
        # with a "delete_event".
        return False

    def destroy(self, widget, data=None):
        print "destroy signal occurred"
        gtk.main_quit()

    def __init__(self):
        # create a new window
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.connect("delete_event", self.delete_event)

        self.window.connect("destroy", self.destroy)

        self.window.set_border_width(10)

        p = subprocess.Popen(["matchbox-keyboard", "--xid"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.keyboard = gtk.Socket()
        self.window.add(self.keyboard)
        self.keyboard.add_id(int(p.stdout.readline()))
        self.keyboard.show()

        self.window.show()



    def main(self):
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        gtk.main()


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
    hello = HelloWorld()
    hello.main()