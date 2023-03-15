import cv2
import os

import pandas as pd

from traits.api import Enum, File, Float, HasTraits, Int, Instance, List
from traitsui.api import HGroup, VGroup, View
from chaco.api import ArrayPlotData, Plot

from easy_dlc_analyzer.panels import config_panel, image_panel, graph_panel

VIDEO_EXT = ".mp4"
HDF_KEYS = [".h5", "filtered.h5"]
CONFIG_EXTS = [f"*{VIDEO_EXT}"]
HDF_LOAD_KEY = "df_with_missing"
DEFAULT_FPS = 30


class AnalyzerView(HasTraits):
    
    video_path = File(filter=CONFIG_EXTS)
    fps = Float(DEFAULT_FPS)
    frame = Int(0)
    max_frame = Int(0)
    
    hdf_keys = List(HDF_KEYS)
    hdf_key = Enum(values="hdf_keys")
    
    parameters = List(["none"])
    parameter = Enum(values="parameters")
    
    image_plot = Instance(Plot)
    graph_plot = Instance(Plot)
    
    def _plot_graph(self):
        x = self.df.index
        y = self.df[self.parameter].values
        graph_data = ArrayPlotData(x=x, y=y)
        plot = Plot(graph_data)
        plot.plot(
            ("x", "y"),
            type="scatter",
            color="red",
            marker="dot",
            marker_size=2
        )
        self.graph_plot = plot
    
    def _plot_image(self):
        image = self._load_frame()
        image_data = ArrayPlotData(image=image)
        plot = Plot(image_data)
        plot.img_plot("image")
        self.image_plot = plot
        
    def _find_hdf(self):
        parent = os.path.dirname(self.video_path)
        file_key = os.path.basename(self.video_path).replace(VIDEO_EXT, "")
        ext_key = self.hdf_key
        hdfs = [file for file in os.listdir(parent) if (file_key in file) and (ext_key in file)]
        return os.path.join(parent, hdfs[0])
    
    def _load_frame(self):
        video = cv2.VideoCapture(self.video_path)
        video.set(cv2.CAP_PROP_POS_FRAMES, self.frame)
        _, image = video.read()
        video.release()
        return image
    
    def _load_hdf(self):
        hdf_path = self._find_hdf()
        df = pd.read_hdf(hdf_path, key=HDF_LOAD_KEY)
        df.columns = [f"{col[1]}_{col[2]}" for col in df.columns]
        
        self.df = df
        self.parameters = df.columns.to_list()
    
    def _load_video(self):
        video = cv2.VideoCapture(self.video_path)
        self.fps = video.get(cv2.CAP_PROP_FPS)
        self.max_frame = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        video.release()
    
    def _video_path_changed(self):
        self._load_video()
        self._load_hdf()
        self._plot_image()
        self._plot_graph()
    
    def _frame_changed(self):
        self._plot_image()
    
    def _parameter_changed(self):
        self._plot_graph()

    traits_view = View(
        VGroup(
            config_panel(),
            HGroup(
                image_panel(),
                graph_panel(),
                layout="split",
            ),
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