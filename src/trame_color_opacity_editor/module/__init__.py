from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_color_opacity_editor": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_color_opacity_editor/trame_color_opacity_editor.umd.js"]

styles = ["__trame_color_opacity_editor/trame_color_opacity_editor.css"]

# List of Vue plugins to install/load
vue_use = ["trame_color_opacity_editor"]


# Optional if you want to execute custom initialization at module load
def setup(server, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    assert server.client_type == "vue3"
