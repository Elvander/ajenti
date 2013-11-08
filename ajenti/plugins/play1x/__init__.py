from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='Play! Framework 1.x',
    icon='play',
    dependencies=[
        BinaryDependency('play'),
        BinaryDependency('java'),
        PluginDependency('main'),
    ],
)


def init():
    import main
