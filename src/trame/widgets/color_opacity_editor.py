from trame_color_opacity_editor.widgets import *  # noqa: F403


def initialize(server):
    from trame_color_opacity_editor import module

    server.enable_module(module)
