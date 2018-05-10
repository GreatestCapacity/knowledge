from .environment import Environment
from os import listdir
from importlib import import_module


def init():
    print('Welcome to Knowledge')
    print('Createst Capacity Presents')
    print('Github: https://github.com/greatestcapacity')
    print('Type "help" for help.')

    env = Environment()

    plugins = listdir('./text_mode/plugins')

    for plugin in plugins:
        module_name = 'text_mode.plugins.' + plugin + '.prelude'
        module = import_module(module_name)
        if hasattr(module, 'prelude'):
            prelude = getattr(module, 'prelude')
            env = prelude(env)

    return env
