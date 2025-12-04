from pathlib import Path

import numpy as np
from PIL import Image
from trame.app import TrameApp
from trame.assets.remote import GoogleDriveFile
from trame.decorators import change
from trame.ui.vuetify3 import VAppLayout
from volume_view import VolumeView

from trame.widgets import color_opacity, html
from trame.widgets import vtk as vtk_widgets
from trame.widgets import vuetify3 as v3

# import matplotlib.cm as cm; import numpy as np; [[float(c) for c in cm.viridis(x)[:3]] for x in np.linspace(0, 1, 16)];
COLORMAPS = {
    "RBG": [[1, 0, 0], [0, 0, 1], [0, 1, 0]],
    "WB": [[1, 1, 1], [0, 0, 0]],
    "viridis": [
        [0.267004, 0.004874, 0.329415],
        [0.282656, 0.100196, 0.42216],
        [0.277134, 0.185228, 0.489898],
        [0.253935, 0.265254, 0.529983],
        [0.221989, 0.339161, 0.548752],
        [0.190631, 0.407061, 0.556089],
        [0.163625, 0.471133, 0.558148],
        [0.139147, 0.533812, 0.555298],
        [0.120565, 0.596422, 0.543611],
        [0.134692, 0.658636, 0.517649],
        [0.20803, 0.718701, 0.472873],
        [0.327796, 0.77398, 0.40664],
        [0.477504, 0.821444, 0.318195],
        [0.647257, 0.8584, 0.209861],
        [0.82494, 0.88472, 0.106217],
        [0.993248, 0.906157, 0.143936],
    ],
    "cividis": [
        [0.0, 0.135112, 0.304751],
        [0.0, 0.18161, 0.421859],
        [0.117612, 0.225935, 0.434308],
        [0.208926, 0.272546, 0.424809],
        [0.279411, 0.318677, 0.423031],
        [0.342246, 0.364939, 0.428559],
        [0.401418, 0.41179, 0.440708],
        [0.458366, 0.459552, 0.460457],
        [0.51792, 0.508454, 0.472707],
        [0.582087, 0.55867, 0.468118],
        [0.648222, 0.610553, 0.454801],
        [0.716177, 0.664384, 0.432386],
        [0.785965, 0.720438, 0.399613],
        [0.857809, 0.778969, 0.353259],
        [0.93218, 0.840159, 0.28588],
        [0.995737, 0.909344, 0.217772],
    ],
    "plasma": [
        [0.050383, 0.029803, 0.527975],
        [0.200445, 0.017902, 0.593364],
        [0.312543, 0.008239, 0.6357],
        [0.417642, 0.000564, 0.65839],
        [0.517933, 0.021563, 0.654109],
        [0.610667, 0.090204, 0.619951],
        [0.69284, 0.165141, 0.564522],
        [0.764193, 0.240396, 0.502126],
        [0.826588, 0.315714, 0.441316],
        [0.881443, 0.392529, 0.383229],
        [0.928329, 0.472975, 0.326067],
        [0.965024, 0.559118, 0.268513],
        [0.98826, 0.652325, 0.211364],
        [0.994141, 0.753137, 0.161404],
        [0.977995, 0.861432, 0.142808],
        [0.940015, 0.975158, 0.131326],
    ],
    "inferno": [
        [0.001462, 0.000466, 0.013866],
        [0.046915, 0.030324, 0.150164],
        [0.142378, 0.046242, 0.308553],
        [0.258234, 0.038571, 0.406485],
        [0.366529, 0.071579, 0.431994],
        [0.472328, 0.110547, 0.428334],
        [0.578304, 0.148039, 0.404411],
        [0.682656, 0.189501, 0.360757],
        [0.780517, 0.243327, 0.299523],
        [0.865006, 0.316822, 0.226055],
        [0.929644, 0.411479, 0.145367],
        [0.970919, 0.522853, 0.058367],
        [0.987622, 0.64532, 0.039886],
        [0.978806, 0.774545, 0.176037],
        [0.950018, 0.903409, 0.380271],
        [0.988362, 0.998364, 0.644924],
    ],
    "jet": [
        [0.0, 0.0, 0.5],
        [0.0, 0.0, 0.803030303030303],
        [0.0, 0.03333333333333333, 1.0],
        [0.0, 0.3, 1.0],
        [0.0, 0.5666666666666667, 1.0],
        [0.0, 0.8333333333333334, 1.0],
        [0.16129032258064513, 1.0, 0.8064516129032259],
        [0.3763440860215053, 1.0, 0.5913978494623656],
        [0.5913978494623655, 1.0, 0.3763440860215054],
        [0.8064516129032256, 1.0, 0.16129032258064513],
        [1.0, 0.9012345679012348, 0.0],
        [1.0, 0.6543209876543212, 0.0],
        [1.0, 0.40740740740740755, 0.0],
        [1.0, 0.16049382716049398, 0.0],
        [0.8030303030303032, 0.0, 0.0],
        [0.5, 0.0, 0.0],
    ],
}

COLORMAP_OPTIONS = list(COLORMAPS.keys())

SHAPER_OPTIONS = ["opacity", "histograms", "full"]


class VolumeApp(TrameApp):
    def __init__(self, image_data, server=None):
        super().__init__(server, client_type="vue3")

        self.state.x_range = [int(np.min(image_data)), int(np.max(image_data))]
        hist, bins = np.histogram(image_data, bins=251)
        hist = np.log10(hist)
        self.state.hist_y_range = [0, float(np.max(hist))]
        self.state.histograms = [[float(bin), float(count)] for count, bin in zip(hist, bins)]
        self.state.opacities = self.make_linear_nodes([0, 1], self.state.x_range)

        self.volume_view = VolumeView()
        self.volume_view.volume_property.SetShade(1)  # enable shadows
        self.volume_view.set_data(image_data)

        # Reset the camera and render
        self.volume_view.renderer.ResetCamera()

        self._build_ui()

    @staticmethod
    def make_linear_nodes(values, range):
        span = range[1] - range[0]
        dx = span / max(len(values) - 1, 1)

        nodes = []

        for i, value in enumerate(values):
            nodes.append([range[0] + i * dx, value])

        return nodes

    @change("colormap_name")
    def on_colormap_name_changed(self, colormap_name, **_):
        self.state.colors = self.make_linear_nodes(COLORMAPS[colormap_name], self.state.x_range)

    @change("opacities")
    def on_opacities_changed(self, opacities, **_):
        pwf = self.volume_view.volume_property.GetScalarOpacity()
        pwf.RemoveAllPoints()
        for node in opacities:
            pwf.AddPoint(node[0], node[1])

        self.ctx.view.update()

    @change("colors")
    def on_colors_changed(self, colors, **_):
        ctf = self.volume_view.volume_property.GetRGBTransferFunction()
        ctf.RemoveAllPoints()
        for node in colors:
            ctf.AddRGBPoint(node[0], *node[1])

        self.ctx.view.update()

    def on_opacity_node_modified(self, _index, _node):
        pass

    def on_opacity_node_added(self, _index, _node):
        pass

    def on_opacity_node_removed(self, _index):
        pass

    def on_color_node_modified(self, _index, _node):
        pass

    def on_color_node_added(self, _index, _node):
        pass

    def on_color_node_removed(self, _index):
        pass

    def _build_ui(self):
        with VAppLayout(self.server) as self.ui:
            with html.Div(classes="d-flex flex-column h-100"):
                with html.Div(classes="d-flex flex-row ga-3 pa-3"):
                    v3.VSelect(
                        v_model=("colormap_name", "RBG"),
                        items=("colormap_options", COLORMAP_OPTIONS),
                        label="ColorMap",
                        flat=True,
                        variant="solo-filled",
                        hide_details=True,
                        density="compact",
                    )
                    v3.VSelect(
                        v_model=("background_shape", "histograms"),
                        items=("background_shape_options", SHAPER_OPTIONS),
                        label="Background Shape",
                        flat=True,
                        variant="solo-filled",
                        hide_details=True,
                        density="compact",
                    )
                    v3.VCheckbox(
                        v_model=("background_opacity", False),
                        label="Background Opacity",
                        hide_details=True,
                        density="compact",
                    )
                    v3.VCheckbox(
                        v_model=("show_histograms", False),
                        label="Show Histograms",
                        hide_details=True,
                        density="compact",
                    )

                color_opacity.ColorOpacityEditor(
                    classes="pa-2 h-25",
                    v_model_colorNodes="colors",
                    v_model_opacityNodes=("opacities",),
                    opacity_node_modified=(self.on_opacity_node_modified, "$event"),
                    opacity_node_added=(self.on_opacity_node_added, "$event"),
                    opacity_node_removed=(self.on_opacity_node_removed, "[$event]"),
                    color_node_modified=(self.on_color_node_modified, "$event"),
                    color_node_added=(self.on_color_node_added, "$event"),
                    color_node_removed=(self.on_color_node_removed, "[$event]"),
                    histograms=("histograms",),
                    scalar_range=("x_range",),
                    histograms_range=("hist_y_range",),
                    show_histograms=("show_histograms",),
                    histograms_color=("histograms_color", [0, 0, 0, 0.25]),
                    background_shape=("background_shape",),
                    background_opacity=("background_opacity",),
                    handle_radius=7,
                    line_width=2,
                    viewport_padding=("viewport_padding", [8, 8]),
                    handle_color=("handle_color", [0.125, 0.125, 0.125, 1]),
                    handle_border_color=("handle_border_color", [0.75, 0.75, 0.75, 1]),
                )

                with html.Div(classes="flex-grow-1"):
                    vtk_widgets.VtkRemoteView(
                        self.volume_view.render_window,
                        interactive_ratio=1,
                        ctx_name="view",
                    )


def main():
    data_file = GoogleDriveFile(
        local_path=Path(__file__).with_name(
            "PtCu_NanoParticles_subsampled_doi_10.1038_sdata.2016.41.tiff"
        ),
        google_id="1hXOQjtdZbFXJGlBnd07H6ATn8nB-oydM",
    )

    # Load the 3D tiff
    frames = []
    img = Image.open(data_file.path)
    for i in range(img.n_frames):
        img.seek(i)
        frames.append(np.array(img))
    image_data = np.array(frames)

    app = VolumeApp(image_data)
    app.server.start()


if __name__ == "__main__":
    main()
