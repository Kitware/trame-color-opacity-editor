from trame_color_opacity.widgets import *  # noqa: F403


def initialize(server):
    from trame_color_opacity import module

    server.enable_module(module)
