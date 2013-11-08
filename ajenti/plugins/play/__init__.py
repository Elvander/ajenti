from ajenti.api import *
from ajenti.plugins import *


info = PluginInfo(
    title='Play! Framework 2.x',
    icon='play',
    dependencies=[
        BinaryDependency('java'),
        PluginDependency('main'),
    ],
)


def init():
    import main
