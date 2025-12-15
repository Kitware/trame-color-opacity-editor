from typing import Sequence
from trame_client.widgets.core import AbstractElement

from trame_color_opacity_editor import module

__all__ = [
    "ColorOpacityEditor",
]


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


def add_named_models(el: HtmlElement, named_models: Sequence[str | tuple[str, str]]):
    for named_model in named_models:
        if isinstance(named_model, tuple):
            python_name, js_name = named_model
        else:
            python_name = named_model
            js_name = named_model

        el._attr_names.append(named_model)
        # TODO: trame bug would ignore js_name if there is an underscore in python_name
        el._attr_names.append((f"v_model_{python_name}", f"v-model:{js_name}"))
        el._event_names.append((f"update_{python_name}", f"update:{js_name}"))


class ColorOpacityEditor(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-color-opacity-editor",
            **kwargs,
        )

        named_models = [
            "colorNodes",
            "opacityNodes",
        ]

        self._attr_names += [
            "histograms",
            ("scalar_range", "scalarRange"),
            ("histograms_range", "histogramsRange"),
            ("background_shape", "backgroundShape"),
            ("background_opacity", "backgroundOpacity"),
            "style",
            ("show_histograms", "showHistograms"),
            ("histograms_color", "histogramsColor"),
            ("viewport_padding", "viewportPadding"),
            ("handle_color", "handleColor"),
            ("handle_border_color", "handleBorderColor"),
            ("handle_radius", "handleRadius"),
            ("line_width", "lineWidth"),
        ]

        self._event_names += [
            ("opacity_node_modified", "opacityNodeModified"),
            ("opacity_node_added", "opacityNodeAdded"),
            ("opacity_node_removed", "opacityNodeRemoved"),
            ("color_node_modified", "colorNodeModified"),
            ("color_node_added", "colorNodeAdded"),
            ("color_node_removed", "colorNodeRemoved"),
        ]

        add_named_models(self, named_models)
