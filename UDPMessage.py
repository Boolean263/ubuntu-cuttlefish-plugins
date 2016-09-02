from cuttlefish.events import CuttleEvent
from cuttlefish.plugins import CuttlePlugin
from cuttlefish.params import StringParam, BoolParam, IntParam

from gi.repository import Gtk, GObject, Notify
import socket
import select
import threading
import re

class UDPMessage(CuttleEvent, CuttlePlugin):
    NAME = "UDP message"
    DESCP = "React upon receipt of a UDP message"
    CATEGORY = "Network"
    PARAMS = {
        'bind' : '0.0.0.0',
        'port' : 50000,
        'content': '',
    }

    class Editor(CuttlePlugin.Editor):
        ORDER = [ 'bind', 'port', 'content' ]

        def begin(self):
            return {
                'bind': StringParam('Listen on address'),
                'port': IntParam('UDP Port'),
                'content': StringParam('Must contain regexp'),
            }

    def __init__(self):
        CuttleEvent.__init__(self)
        CuttlePlugin.__init__(self)

        # I'll use these to tell our thread it should stop listening.
        # When I write to Marco, Polo in the select statement will hear it
        # and exit the loop.
        self._marco, self._polo = socket.socketpair()

    # This function will be spun off into its own thread.
    def _monitor(self):
        inputs = [ self._sock, self._polo ]
        timeout = 60
        do_loop = True
        while do_loop:
            inready, outready, errorready = select.select(inputs, [], [], timeout)
            for s in inready:
                if s == self._sock:
                    data, address = self._sock.recvfrom(4096)
                    src_host, src_port = address
                    if self._params["content"] == "" or re.search(self._params["content"], data):
                        self.trigger()
                elif s == self._polo:
                    data = self._polo.recv(4096)
                    do_loop = False

    def setup(self):
        try:
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._sock.bind((self._params['bind'], int(self._params['port'])))
            self._sock.setblocking(0)
            self._thread = threading.Thread(target=self._monitor)
            self._thread.start()
        except Exception as ex:
            self._thread = None
            Notify.Notification.new('UDP Message Plugin error', ex.args[1]).show()

    def teardown(self):
        if self._thread is not None:
            self._marco.send("bye")
            self._thread.join(5)
        self._thread = None

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
