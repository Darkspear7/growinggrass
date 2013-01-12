#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

def timeout_disable(widget, onEvent, seconds):
    true_seconds = seconds * 1000
    def disableWidget(widget, data=None):
        def enableWidget():
            widget.set_sensitive(True)

        widget.set_sensitive(False)
        gobject.timeout_add(true_seconds, enableWidget)

    widget.connect(onEvent, disableWidget, None)
    


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
    
        self.button = gtk.Button("Can be disabled")
        timeout_disable(self.button, 'clicked', 10)
    
        self.window.add(self.button)
        self.button.show()
        self.window.show()

    def main(self):
        gtk.main()

if __name__ == "__main__":
    delayed = DelayedButton()
    delayed.main()

