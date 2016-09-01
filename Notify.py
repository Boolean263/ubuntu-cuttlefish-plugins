from cuttlefish.actions import CuttleAction
from cuttlefish.plugins import CuttlePlugin
from cuttlefish.params import StringParam, SelectParam, BoolParam, FileParam

from gi.repository import GObject, Notify, GdkPixbuf

class NotifySender(CuttleAction, CuttlePlugin):
    NAME = 'Show Notification'
    DESCP = 'Show pop-up notification'
    CATEGORY = 'Your Plugins'
    PARAMS = {
        'title'     : 'Notification title',
        'body'      : 'Notification body',
        'urgency'   : 1,
        'use_image' : False,
        'image'     : '',
    }

    class Editor(CuttlePlugin.Editor):
        ORDER = ['title', 'body', 'urgency', 'use_image', 'image']

        def begin(self):
            return {
                'title'     : StringParam('Title'),
                'body'      : StringParam('Body'),
                'urgency'   : SelectParam('Urgency', {
                                0: 'Low',
                                1: 'Default',
                                2: 'High',
                            }, int),
                'use_image' : BoolParam('With Image'),
                'image'     : FileParam('Image'),
            }

    def __init__(self):
        CuttleAction.__init__(self)
        CuttlePlugin.__init__(self)

    def execute(self):
        n = Notify.Notification.new(self._params['title'],
            self._params['body'])
        n.set_urgency(self._params['urgency'])
        if self._params['use_image'] and self._params['image']:
            image = GdkPixbuf.Pixbuf.new_from_file(self._params['image'])
            n.set_icon_from_pixbuf(image)
            n.set_image_from_pixbuf(image)
        n.show()

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
