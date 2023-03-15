import cv2
import os

import pandas as pd

from traits.api import Enum, File, Float, HasTraits, Int, Instance, List
from traitsui.api import VGroup, View
from chaco.api import ArrayPlotData, Plot

from easy_dlc_analyzer.panels import config_panel, image_panel

VIDEO_EXT = ".mp4"
HDF_KEYS = [".h5", "filtered.h5"]
CONFIG_EXTS = [f"*{VIDEO_EXT}"]
HDF_LOAD_KEY = "df_with_missing"
FPS = 30


class AnalyzerView(HasTraits):
    
    video_path = File(filter=CONFIG_EXTS)
    
    fps = Float(FPS)
    
    hdf_keys = List(HDF_KEYS)
    
    hdf_key = Enum(values="hdf_keys")
    
    image_plot = Instance(Plot)
    
    frame = Int(1)
    
    def _load_frame(self):
        video = cv2.VideoCapture(self.video_path)
        video.set(cv2.CAP_PROP_POS_FRAMES, int(self.frame))
        _, image = video.read()
        video.release()
        return image
    
    def _plot_image(self):
        image = self._load_frame()
        image_data = ArrayPlotData(image=image)
        plot = Plot(image_data)
        plot.img_plot("image")
        return plot
    
    def _find_hdf(self):
        parent = os.path.dirname(self.video_path)
        file_key = os.path.basename(self.video_path).replace(VIDEO_EXT, "")
        ext_key = self.hdf_key
        hdfs = [file for file in os.listdir(parent) if (file_key in file) and (ext_key in file)]
        return os.path.join(parent, hdfs[0])
    
    def _load_hdf(self):
        hdf_path = self._find_hdf()
        df = pd.read_hdf(hdf_path, key=HDF_LOAD_KEY)
        df.columns = [f"{col[1]}_{col[2]}" for col in df.columns]
        self.df = df
    
    def _video_path_changed(self):
        self._load_hdf()
        self._plot_image()
    
    def _frame_changed(self):
        self._plot_image()

    traits_view = View(
        VGroup(
            config_panel(),
            image_panel(),
            # graph_panel(),
            # export_panel(),
        ),
        title="Easy DLC Analyzer",
        width=1920,
        height=1080,
        resizable=True,
    )

def main():
    
    analyzer_view = AnalyzerView()

    analyzer_view.configure_traits()


if __name__ == "__main__":
    main()