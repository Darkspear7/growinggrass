#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

def timeout_uncheck(widget, onEvent, seconds):
    true_seconds = seconds * 1000
    def toggleWidget(widget, data=None):
        def swapWidget():
            widget.set_active(not widget.get_active())

        gobject.timeout_add(true_seconds, swapWidget)

    widget.connect(onEvent, toggleWidget, None)
    


class DelayedButton:

    def delete_event(self, widget, event, data=None):
        return False

    def destroy(self, widget, data=None):
        gtk.main_quit()

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
    
        self.window.connect("delete_event", self.delete_event)
        self.window.connect("destroy", self.destroy)
        self.window.set_border_width(10)
    
        self.checkbox = gtk.ToggleButton()
        timeout_uncheck(self.checkbox, 'toggled', 10)
    
        self.window.add(self.checkbox)
        self.checkbox.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    delayed = DelayedButton()
    delayed.main()

