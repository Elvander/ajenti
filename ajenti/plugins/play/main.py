from ajenti.api import *
from ajenti.plugins.configurator.api import ClassConfigEditor
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder

@plugin
class PlayFrameworkClassConfigEditor (ClassConfigEditor):
    title = _('PlayFramework')
    icon = 'play'

    def init(self):
        self.append(self.ui.inflate('play:config'))

@plugin
class PlayFramework (SectionPlugin):
    default_classconfig = {'libfolder': '/home/bart/'}
    classconfig_editor = PlayFrameworkClassConfigEditor
    classconfig_root = True

    def init(self):
        self.title = 'Play'
        self.icon = 'play'
        self.category = 'Applications'

        self.append(self.ui.inflate('play:main'))
        self.find('style').labels = self.find('style').values = ['info', 'warning', 'error']

    @on('show', 'click')
    def on_show(self):
        self.context.notify(self.find('style').value, self.find('text').value)
