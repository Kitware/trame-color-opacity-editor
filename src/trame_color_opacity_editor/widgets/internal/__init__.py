from trame_color_opacity_editor.widgets import HtmlElement, add_named_models


class ViewportContainer(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-viewport-container",
            **kwargs,
        )

        self._attr_names += []

        self._event_names += []

        slot_props = [
            "viewportSize",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'


class NodeMerger(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-node-merger",
            **kwargs,
        )

        self._attr_names += [
            ("color_nodes", "colorNodes"),
            ("opacity_nodes", "opacityNodes"),
        ]

        self._event_names += []

        slot_props = [
            "colorOpacityNodes",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'


class BackgroundView(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-view",
            **kwargs,
        )

        self._attr_names += [
            "size",
            "padding",
            "nodes",
            "shape",
        ]

        self._event_names += []


class ControlsView(HtmlElement):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-controls-view",
            **kwargs,
        )

        named_models = [
            "nodes",
        ]

        self._attr_names += [
            "size",
            "padding",
            "radius",
            ("show_line", "showLine"),
            ("line_width", "lineWidth"),
        ]

        self._event_names += [
            ("node_modified", "nodeModified"),
            ("node_added", "nodeAdded"),
            ("node_removed", "nodeRemoved"),
        ]

        add_named_models(self, named_models)


class NodeFlattener(HtmlElement):
    FLATTENED_NODES_SLOT_PROP = "flattenedNodes"

    def __init__(
        self,
        flattened_nodes_slot_prop=FLATTENED_NODES_SLOT_PROP,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-node-flattener",
            **kwargs,
        )

        self._attr_names += []

        self._event_names += [
            ("node_modified", "nodeModified"),
            ("node_added", "nodeAdded"),
            ("node_removed", "nodeRemoved"),
        ]

        named_models = [
            "nodes",
        ]

        add_named_models(self, named_models)

        slot_props = {
            "flattenedNodes": flattened_nodes_slot_prop,
            "flattenedNodesUpdated": f"{flattened_nodes_slot_prop}Updated",
            "flattenedNodeModified": f"{flattened_nodes_slot_prop}NodeModified",
            "flattenedNodeAdded": f"{flattened_nodes_slot_prop}NodeAdded",
            "flattenedNodeRemoved": f"{flattened_nodes_slot_prop}NodeRemoved",
        }

        self._attributes["slot"] = (
            f'v-slot="{{ { ", ".join(map(lambda it: f"{it[0]}:{it[1]}", slot_props.items())) } }}"'
        )


class BaseShaper(HtmlElement):
    def __init__(
        self,
        tag,
        **kwargs,
    ):
        super().__init__(
            tag,
            **kwargs,
        )

        slot_props = [
            "shape",
        ]
        self._attributes["slot"] = f'v-slot="{{ {", ".join(slot_props)} }}"'


class BackgroundShaperFull(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-full",
            **kwargs,
        )


class BackgroundShaperOpacity(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-opacity",
            **kwargs,
        )

        self._attr_names += [
            "nodes",
        ]


class BackgroundShaperHistograms(BaseShaper):
    def __init__(
        self,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-background-shaper-histograms",
            **kwargs,
        )

        self._attr_names += [
            "nodes",
        ]


class NodeScaler(HtmlElement):
    SCALED_NODES_SLOT_PROP = "scaledNodes"

    def __init__(
        self,
        scaled_nodes_slot_prop=SCALED_NODES_SLOT_PROP,
        **kwargs,
    ):
        super().__init__(
            "trame-coe-node-scaler",
            **kwargs,
        )

        self._attr_names += [
            ("x_range", "xRange"),
            ("y_range", "yRange"),
        ]

        self._event_names += [
            ("node_modified", "nodeModified"),
            ("node_added", "nodeAdded"),
            ("node_removed", "nodeRemoved"),
        ]

        named_models = [
            "nodes",
        ]

        add_named_models(self, named_models)

        slot_props = {
            "scaledNodes": scaled_nodes_slot_prop,
            "scaledNodesUpdated": f"{scaled_nodes_slot_prop}Updated",
            "scaledNodeModified": f"{scaled_nodes_slot_prop}NodeModified",
            "scaledNodeAdded": f"{scaled_nodes_slot_prop}NodeAdded",
            "scaledNodeRemoved": f"{scaled_nodes_slot_prop}NodeRemoved",
        }

        self._attributes["slot"] = (
            f'v-slot="{{ { ", ".join(map(lambda it: f"{it[0]}:{it[1]}", slot_props.items())) } }}"'
        )
