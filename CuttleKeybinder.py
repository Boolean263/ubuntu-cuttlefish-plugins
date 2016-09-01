from cuttlefish.events import CuttleEvent
from cuttlefish.plugins import CuttlePlugin
from cuttlefish.params import StringParam

import gi
gi.require_version('Keybinder', '3.0')
from gi.repository import Gtk, GObject, Keybinder

class CuttleKeybinder(CuttleEvent, CuttlePlugin):
    NAME = "Keybinder"
    DESCP = "Act on user-defined hotkey"
    CATEGORY = "Window Manager"
    PARAMS = {
        'hotkey' : '<Ctrl><Shift>F1',
    }

    class Editor(CuttlePlugin.Editor):
        ORDER = [ 'hotkey' ]

        def begin(self):
            return {
                'hotkey': StringParam('Key combination'),
            }

    # Do I need this?
    def __init__(self):
        CuttleEvent.__init__(self)
        CuttlePlugin.__init__(self)

    def handle_keypress(self, keypress, data):
        self.trigger()

    def setup(self):
        Keybinder.init()
        Keybinder.bind(self._params['hotkey'], self.handle_keypress, None)

    def teardown(self):
        Keybinder.unbind(self._params['hotkey'])

#
# Editor modelines  -  https://www.wireshark.org/tools/modelines.html
#
# Local variables:
# c-basic-offset: 4
# tab-width: 4
# indent-tabs-mode: nil
# coding: utf8
# mode: python
# End:
#
# vi: set shiftwidth=4 tabstop=4 expandtab fileencoding=utf8 filetype=python:
# :indentSize=4:tabSize=4:noTabs=true:coding=utf8:mode=python:
#
