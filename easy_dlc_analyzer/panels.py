from traitsui.api import HGroup, Item, VGroup
from enable.api import ComponentEditor


def config_panel():
    config_panel = VGroup(
        Item("video_path", label="HDF Path"),
        HGroup(
            Item("fps", label="FPS", width=200),
            Item("hdf_key", label="HDF ext", width=200)
        ),
    )
    return config_panel


def image_panel():
    image_panel = VGroup(
        Item("image_plot", editor=ComponentEditor()),
        Item("frame", label="Postion of frame")
    )
    return image_panel
