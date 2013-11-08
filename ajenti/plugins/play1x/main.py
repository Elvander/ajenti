import os
import logging
import subprocess

from ajenti.api import *
from ajenti.plugins.configurator.api import ClassConfigEditor
from ajenti.plugins.main.api import SectionPlugin
from ajenti.ui import on
from ajenti.ui.binder import Binder


class Application(object):

    def __init__(self, name, appFolder):
        self.name = str(name)
        self.appFolder = appFolder
        self.status = self.getStatus()
        logging.debug("Name: %s" % self.name)

    def getStatus(self):
        if self.running:
            return "Running"
        else:
            return "Not active"

    @property
    def icon(self):
        return 'play' if self.running else None

    @property
    def running(self):
        path = os.path.join(self.appFolder, self.name, "server.pid")
        return os.path.exists(path)

    def start(self):
        command = 'start %s' % os.path.join(self.appFolder, self.name)
        logging.debug(command)
        pid = subprocess.Popen(['play', command]).pid
        logging.debug("start application [%s]: %s" % (self.name, pid))

    def restart(self):
        logging.debug("Restart application [%s]" % self.name)

    def stop(self):
        command = 'stop %s' % os.path.join(self.appFolder, self.name)
        logging.debug(command)
        subprocess.call(['play', command])
        logging.debug("Stop application [%s]" % self.name)


@plugin
class PlayFramework1ClassConfigEditor (ClassConfigEditor):
    title = _('PlayFramework1x')
    icon = 'play'

    def init(self):
        self.append(self.ui.inflate('play1x:config'))


@plugin
class PlayFramework1 (SectionPlugin):
    default_classconfig = {'libfolder.v1': '/home/bart/playapps/v1/'}
    classconfig_editor = PlayFramework1ClassConfigEditor
    classconfig_root = True

    def init(self):
        self.title = 'Play! Framework 1.x'
        self.icon = 'play'
        self.category = 'Applications'

        self.appFolder = self.classconfig['libfolder.v1']
        self.append(self.ui.inflate('play1x:main'))
        self.binder = Binder(None, self)

        def post_item_bind(object, collection, item, ui):
            ui.find('stop').on('click', self.on_stop, item)
            ui.find('restart').on('click', self.on_restart, item)
            ui.find('start').on('click', self.on_start, item)
            ui.find('stop').visible = item.running
            ui.find('restart').visible = item.running
            ui.find('start').visible = not item.running

        self.find('collection').post_item_bind = post_item_bind

    def on_page_load(self):
        self.refresh()

    def on_start(self, item):
        item.start()
        self.refresh()
        self.context.notify('info', _('%s started') % item.name)

    def on_stop(self, item):
        item.stop()
        self.refresh()
        self.context.notify('info', _('%s stopped') % item.name)

    def on_restart(self, item):
        item.restart()
        self.refresh()
        self.context.notify('info', _('%s restarted') % item.name)

    def refresh(self):
        self.applications = [Application(x, self.appFolder) for x in self.loadApplication()]
        self.binder.reset(self).autodiscover().populate()

    def loadApplication(self):
        return os.listdir(self.appFolder)
