from tkinter import *
from view.app import MenuBar
from view.images import PageImages
from view.reportPage import Report
from view.processing.thresholding import Thresholding
from view.processing.regionGrowing import RegionGrowing
from view.processing.kmeans import Kmeans
from view.processing.gmm import GMM
from view.preprocessing.filters.meanFilter import MeanFilter
from view.preprocessing.filters.medianFilter import MedianFilter
from view.preprocessing.filters.edgeFilter import EdgeFilter
from view.preprocessing.intensities.rescaled import Rescaled
from view.preprocessing.intensities.zscore import Zscore
from view.preprocessing.intensities.whiteStripe import WhiteStripe
from view.preprocessing.intensities.matching import Matching
from view.histograms import Histograms
from view.registration import Registration
from view.preprocessing.removalSkull import Removal
from models.images import Images

class Manager(Tk):

    def __init__(self, *args, **kwargs):

        Tk.__init__(self, *args, **kwargs)
        self.title("Procesador de MRI")
        main_frame = Frame(self, bg="#BEB2A7", )
        main_frame.pack_propagate(0)
        main_frame.pack(fill="both", expand="true")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        self.resizable(0, 0) #prevents the app from being resized
        self.geometry("1024x650")# fixes the applications size
        self.frames = {}
        self.pages = {"PageImages" : PageImages, 
                      "Thresholding" : Thresholding, 
                      "RegionGrowing" : RegionGrowing, 
                      "Kmeans" : Kmeans, 
                      "GMM" : GMM, 
                      "MeanFilter" : MeanFilter,
                      "MedianFilter" : MedianFilter,
                      "EdgeFilter" : EdgeFilter, 
                      "Rescaled" : Rescaled,
                      "Zscore" : Zscore,
                      "WhiteStripe" : WhiteStripe,
                      "Matching" : Matching,
                      "Histograms" : Histograms,
                      "Registration" : Registration,
                      "Removal" : Removal,
                      "Report" : Report}
        for key, F in self.pages.items():
            frame = F(main_frame, self)
            self.frames[key] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("PageImages")
        menubar = MenuBar(self)
        Tk.config(self, menu=menubar)


    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, 'combobox_imgs'):
            frame.combobox_imgs['values'] =Images().load_data_combobox("combobox_imgs")
        if hasattr(frame, 'combobox_template'):
            frame.combobox_template['values'] =Images().load_data_combobox("combobox_imgs")
        frame.tkraise()


