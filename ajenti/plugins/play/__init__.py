from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='Play! Framework',
    icon='play',
    dependencies=[
        PluginDependency('main'),
    ],
)


def init():
    import main
