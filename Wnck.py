from cuttlefish.events import CuttleEvent
from cuttlefish.plugins import CuttlePlugin
from cuttlefish.params import StringParam, SelectParam

from cuttlefish.plugins.run import WnckScreenMonitor

import gi
gi.require_version('Wnck', '3.0')
from gi.repository import Wnck

################################
class WnckEventPlugin(CuttlePlugin):
    PARAMS = {
        'label': None,
        'name': '',
        'type': '',
        'role': '',
        'app' : '',
    }

    class Editor(CuttlePlugin.Editor):
        ORDER = [ 'app', 'name', 'type', 'role' ]
        def begin(self):
            return {
                'name': StringParam('Window Name'),
                'type': StringParam('Window Type'),
                'role': StringParam('Window Role'),
                'app' : StringParam('Application Name'),
            }

    def __init__(self, event):
        WnckScreenMonitor.__init__(self, event)
        CuttlePlugin.__init__(self)

    def on_screen_event(self, screen, data):
        if data is None: return
        hit = {
            'name': str(data.get_name()),
            'type': str(data.get_class_instance_name()),
            'role': str(data.get_role()),
            'app' : str(data.get_application().get_name()),
        }
        if (self._params['name'] == '' or self._params['name'] == hit['name']) and \
           (self._params['type'] == '' or self._params['type'] == hit['type']) and \
           (self._params['role'] == '' or self._params['role'] == hit['role']) and \
           (self._params['app'] == '' or self._params['app'] == hit['app']):
            self.trigger()

################################
class WindowOpen(WnckScreenMonitor, WnckEventPlugin):
    CATEGORY="Window Manager"
    NAME = 'Window opens'
    DESCP = 'React when a specified window opens'

    def __init__(self):
        WnckEventPlugin.__init__(self, 'window-opened')

################################
class WindowClose(WnckScreenMonitor, WnckEventPlugin):
    CATEGORY="Window Manager"
    NAME = 'Window closes'
    DESCP = 'React when a specified window closes'

    def __init__(self):
        WnckEventPlugin.__init__(self, 'window-closed')

################################
class WindowFocusBlur(WnckScreenMonitor, WnckEventPlugin):
    CATEGORY="Window Manager"
    NAME = 'Window focus'
    DESCP = 'React when a specified window gains or loses focus'
    PARAMS = {
        'label': '',
        'focus': True,
        'name': '',
        'type': '',
        'role': '',
        'app' : '',
    }

    class Editor(CuttlePlugin.Editor):
        ORDER = [ 'focus', 'app', 'name', 'type', 'role' ]
        def begin(self):
            return {
                'focus': SelectParam('Event', {
                    False: 'Window loses focus',
                    True: 'Window gains focus',
                }, bool),
                'name': StringParam('Window Name'),
                'type': StringParam('Window Type'),
                'role': StringParam('Window Role'),
                'app' : StringParam('Application Name'),
            }

    def __init__(self):
        WnckEventPlugin.__init__(self, 'active-window-changed')
        CuttlePlugin.__init__(self)

    def on_screen_event(self, screen, data):
        if self._params['focus']:
            WnckEventPlugin.on_screen_event(self, screen, screen.get_active_window())
        else:
            WnckEventPlugin.on_screen_event(self, screen, data)

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
