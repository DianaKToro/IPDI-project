from tkinter import *

class MenuBar(Menu):
    def __init__(self, parent):
        Menu.__init__(self, parent)
        self.controller = parent
        self.add_command( label="Imágenes", command=lambda: parent.show_frame("PageImages"))

        menu_preprocessing = Menu(self, tearoff=0)
        self.add_cascade(label="Preprocesamiento", menu=menu_preprocessing)
        menu_preprocessing.add_command(label="Remoción del cráneo", command=lambda: parent.show_frame("Removal"))

        menu_intensities = Menu(menu_preprocessing, tearoff=0)
        menu_preprocessing.add_cascade(label="Estandarización de intensidades", menu=menu_intensities)
        menu_intensities.add_command(label="Rescalado", command=lambda: parent.show_frame("Rescaled"))
        menu_intensities.add_command(label="Z-score", command=lambda: parent.show_frame("Zscore"))
        menu_intensities.add_command(label="White stripe", command=lambda: parent.show_frame("WhiteStripe"))
        menu_intensities.add_command(label="Coincidencia de histogramas", command=lambda: parent.show_frame("Matching"))

        menu_filters = Menu(menu_preprocessing, tearoff=0)
        menu_preprocessing.add_cascade(label="Remoción del ruido", menu=menu_filters)
        menu_filters.add_command(label="Filtro promedio", command=lambda: parent.show_frame("MeanFilter"))
        menu_filters.add_command(label="Filtro mediano", command=lambda: parent.show_frame("MedianFilter"))
        menu_filters.add_command(label="Detección de bordes", command=lambda: parent.show_frame("EdgeFilter"))

        menu_segmentation = Menu(self, tearoff=0)
        self.add_cascade(label="Segmentación", menu=menu_segmentation)
        menu_segmentation.add_command(label="Umbralización",command=lambda: parent.show_frame("Thresholding"))
        menu_segmentation.add_command(label="Crecimiento de regiones", command=lambda: parent.show_frame("RegionGrowing"))
        menu_segmentation.add_command(label="K-means", command=lambda: parent.show_frame("Kmeans"))
        menu_segmentation.add_command(label="GMM", command=lambda: parent.show_frame("GMM"))

        self.add_command(label="Histogramas", command=lambda: parent.show_frame("Histograms"))
        self.add_command(label="Registro", command=lambda: parent.show_frame("Registration"))
        self.add_command(label="Reporte", command=lambda: parent.show_frame("Report"))

    
    def switchButtonState(self):
        if (self.segmentation_button['state'] == NORMAL):
            self.segmentation_button['state'] = DISABLED
            self.segmentation_button['bg'] = 'white'
        else:
            self.segmentation_button['state'] = NORMAL

class GUI(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.main_frame = Frame(self, bg="#BEB2A7", height=600, width=1024)
        # self.main_frame.pack_propagate(0)
        self.main_frame.pack(fill="both", expand="true")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)


